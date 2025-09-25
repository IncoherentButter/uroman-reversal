#!/usr/bin/env python3

"""
Reverse Uroman - Converts Latin script to non-Latin scripts
Written by [Your Name] based on Uroman by Ulf Hermjakob, USC/ISI

This is a reverse implementation of the Uroman system that can convert
Latin text to various non-Latin scripts (Arabic, Devanagari, etc.)
"""

from __future__ import annotations
import argparse
from collections import defaultdict
import datetime
from enum import Enum
import json
import os
from pathlib import Path
import regex
import sys
from typing import List, Tuple, Dict, Optional, Set
import unicodedata as ud

__version__ = '1.0.0'
__last_mod_date__ = 'December 2024'
__description__ = "Reverse Uroman - converts Latin script to non-Latin scripts"

class ReverseRomFormat(Enum):
    """Output format of reverse romanization"""
    STR = 'str'          # simple string
    EDGES = 'edges'      # list of edges (includes character offsets in original string)
    ALTS = 'alts'        # lattice including alternative edges
    LATTICE = 'lattice'  # lattice including alternative and superseded edges

    def __str__(self):
        return self.value

class ReverseRomRule:
    """Reverse romanization rule - maps Latin to non-Latin script"""
    def __init__(self, latin: str, target: str, script: str, **kwargs):
        self.latin = latin  # Latin source text
        self.target = target  # Target script text
        self.script = script  # Target script name
        self.provenance = kwargs.get('provenance', 'manual')
        self.language_codes = kwargs.get('language_codes', [])
        self.priority = kwargs.get('priority', 0)  # Higher = more specific
        self.context_rules = kwargs.get('context_rules', {})
        self.alternatives = kwargs.get('alternatives', [])

    def __str__(self):
        return f"{self.latin} → {self.target} ({self.script})"

class ReverseScript:
    """Information about a target script for reverse romanization"""
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.direction = kwargs.get('direction', 'left-to-right')
        self.default_vowels = kwargs.get('default_vowels', [])
        self.vowel_insertion_rules = kwargs.get('vowel_insertion_rules', {})
        self.character_properties = kwargs.get('character_properties', {})

class ReverseUroman:
    """Main class for reverse romanization - converts Latin to non-Latin scripts"""
    
    def __init__(self, data_dir: Path | None = None, **args):
        self.data_dir = data_dir or self.default_data_dir(**args)
        
        # Core data structures
        self.reverse_rules = defaultdict(list)  # latin_text -> [ReverseRomRule]
        self.scripts = defaultdict(ReverseScript)
        self.latin_prefixes = defaultdict(bool)  # For efficient lookup
        
        # Caching
        self.reverse_cache = {}
        self.cache_size = 0
        self.max_cache_size = args.get('cache_size', 65536)
        
        # Load data files
        self.load_reverse_romanization_data()
        self.load_script_definitions()
        
    @staticmethod
    def default_data_dir(**args) -> Path:
        root_dir = Path(__file__).parent
        data_dir = (root_dir / "reverse_data").resolve()
        if args.get('verbose'):
            sys.stderr.write(f"reverse_data_dir: {str(data_dir)}\n")
        return data_dir
    
    def load_reverse_romanization_data(self):
        """Load reverse romanization rules from data files"""
        # Load Arabic reverse rules
        arabic_file = self.data_dir / "reverse_arabic.txt"
        if arabic_file.exists():
            self.load_reverse_script_file(arabic_file, "Arabic")
        
        # Load Swahili reverse rules
        swahili_file = self.data_dir / "reverse_swahili.txt"
        if swahili_file.exists():
            self.load_reverse_script_file(swahili_file, "Swahili")
        
        # Load general reverse rules
        general_file = self.data_dir / "reverse_general.txt"
        if general_file.exists():
            self.load_reverse_script_file(general_file, "General")
    
    def load_reverse_script_file(self, filename: Path, script_name: str):
        """Load reverse romanization rules for a specific script"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    # Parse line format: latin::target::script::priority::context
                    parts = line.split('::')
                    if len(parts) >= 3:
                        latin = parts[0].strip()
                        target = parts[1].strip()
                        script = parts[2].strip()
                        priority = int(parts[3].strip()) if len(parts) > 3 else 0
                        
                        # Create rule
                        rule = ReverseRomRule(
                            latin=latin,
                            target=target,
                            script=script,
                            priority=priority
                        )
                        
                        self.reverse_rules[latin].append(rule)
                        self.register_latin_prefix(latin)
                        
        except FileNotFoundError:
            sys.stderr.write(f'Cannot open reverse romanization file: {filename}\n')
    
    def load_script_definitions(self):
        """Load script definitions and properties"""
        # Arabic script
        arabic_script = ReverseScript(
            name="Arabic",
            direction="right-to-left",
            default_vowels=["a", "i", "u"],
            vowel_insertion_rules={
                "consonant_final": "a",  # Add 'a' after final consonants
                "consonant_medial": "i",  # Add 'i' between consonants
            }
        )
        self.scripts["Arabic"] = arabic_script
        
        # Devanagari script
        devanagari_script = ReverseScript(
            name="Devanagari",
            direction="left-to-right",
            default_vowels=["a"],
            vowel_insertion_rules={
                "consonant_final": "a",
                "consonant_medial": "a",
            }
        )
        self.scripts["Devanagari"] = devanagari_script
        
        # Swahili script
        swahili_script = ReverseScript(
            name="Swahili",
            direction="left-to-right",
            default_vowels=["a", "i", "u"],
            vowel_insertion_rules={
                "consonant_final": "a",
                "consonant_medial": "i",
            },
            character_properties={
                "has_tone_marks": False,
                "uses_diacritics": False,
                "script_family": "Bantu",
                "loanword_languages": ["Arabic", "English", "Portuguese"]
            }
        )
        self.scripts["Swahili"] = swahili_script
    
    def register_latin_prefix(self, latin: str):
        """Register all prefixes of a Latin string for efficient lookup"""
        for prefix_len in range(1, len(latin) + 1):
            self.latin_prefixes[latin[:prefix_len]] = True
    
    def reverse_romanize_string(self, latin_text: str, target_script: str = "Arabic", 
                               format: ReverseRomFormat = ReverseRomFormat.STR, **args) -> str | List:
        """Main entry point for reverse romanization"""
        
        # Check cache first
        cache_key = (latin_text, target_script, format)
        if cache_key in self.reverse_cache:
            return self.reverse_cache[cache_key]
        
        # Create reverse lattice
        lattice = ReverseLattice(latin_text, self, target_script)
        lattice.build_reverse_lattice()
        
        # Get result based on format
        if format == ReverseRomFormat.STR:
            result = lattice.get_best_reverse_path()
        elif format == ReverseRomFormat.EDGES:
            result = lattice.get_best_edges()
        elif format == ReverseRomFormat.LATTICE:
            result = lattice.get_all_edges()
        else:
            result = lattice.get_best_reverse_path()
        
        # Cache result
        if self.cache_size < self.max_cache_size:
            self.reverse_cache[cache_key] = result
            self.cache_size += 1
        
        return result

class ReverseEdge:
    """Edge in the reverse romanization lattice"""
    def __init__(self, start: int, end: int, latin: str, target: str, script: str, annotation: str = ""):
        self.start = start
        self.end = end
        self.latin = latin  # Original Latin text
        self.target = target  # Target script text
        self.script = script
        self.annotation = annotation
    
    def __str__(self):
        return f'[{self.start}-{self.end}] {self.latin} → {self.target} ({self.script})'

class ReverseLattice:
    """Lattice for reverse romanization - finds best Latin to non-Latin mappings"""
    
    def __init__(self, latin_text: str, reverse_uroman: ReverseUroman, target_script: str):
        self.latin_text = latin_text
        self.reverse_uroman = reverse_uroman
        self.target_script = target_script
        self.edges = defaultdict(list)  # position -> [ReverseEdge]
        self.max_vertex = len(latin_text)
    
    def build_reverse_lattice(self):
        """Build the reverse romanization lattice"""
        # Add edges for all possible Latin spans
        for start in range(self.max_vertex):
            for end in range(start + 1, self.max_vertex + 1):
                latin_span = self.latin_text[start:end]
                
                # Check if this span has reverse romanization rules
                if latin_span in self.reverse_uroman.reverse_rules:
                    rules = self.reverse_uroman.reverse_rules[latin_span]
                    
                    # Find the best rule for our target script
                    best_rule = self.find_best_rule(rules)
                    if best_rule:
                        edge = ReverseEdge(
                            start=start,
                            end=end,
                            latin=latin_span,
                            target=best_rule.target,
                            script=best_rule.script,
                            annotation=f"reverse_{best_rule.provenance}"
                        )
                        self.edges[start].append(edge)
        
        # Add fallback edges for single characters
        for i, char in enumerate(self.latin_text):
            if char.isalpha():
                # Create fallback edge for single Latin characters
                fallback_target = self.get_fallback_target(char)
                edge = ReverseEdge(
                    start=i,
                    end=i+1,
                    latin=char,
                    target=fallback_target,
                    script=self.target_script,
                    annotation="fallback"
                )
                self.edges[i].append(edge)
            else:
                # Preserve non-alphabetic characters (spaces, punctuation, etc.)
                edge = ReverseEdge(
                    start=i,
                    end=i+1,
                    latin=char,
                    target=char,  # Pass through unchanged
                    script="Latin",  # Mark as Latin since it's not being converted
                    annotation="preserve"
                )
                self.edges[i].append(edge)
    
    def find_best_rule(self, rules: List[ReverseRomRule]) -> Optional[ReverseRomRule]:
        """Find the best reverse romanization rule"""
        if not rules:
            return None
        
        # Filter by target script
        script_rules = [r for r in rules if r.script == self.target_script]
        if not script_rules:
            return None
        
        # Return rule with highest priority
        return max(script_rules, key=lambda r: r.priority)
    
    def get_fallback_target(self, char: str) -> str:
        """Get fallback target for a single Latin character"""
        # Simple fallback mapping for Arabic
        if self.target_script == "Arabic":
            fallback_map = {
                'a': 'ا', 'b': 'ب', 'c': 'س', 'd': 'د', 'e': 'ي',
                'f': 'ف', 'g': 'ج', 'h': 'ه', 'i': 'ي', 'j': 'ج',
                'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن', 'o': 'و',
                'p': 'ب', 'q': 'ق', 'r': 'ر', 's': 'س', 't': 'ت',
                'u': 'و', 'v': 'ف', 'w': 'و', 'x': 'كس', 'y': 'ي', 'z': 'ز'
            }
            return fallback_map.get(char.lower(), char)
        
        # Fallback mapping for Swahili (mostly same as Latin)
        elif self.target_script == "Swahili":
            fallback_map = {
                'a': 'a', 'b': 'b', 'c': 'ch', 'd': 'd', 'e': 'e',
                'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j',
                'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o',
                'p': 'p', 'q': 'k', 'r': 'r', 's': 's', 't': 't',
                'u': 'u', 'v': 'v', 'w': 'w', 'x': 'ks', 'y': 'y', 'z': 'z'
            }
            return fallback_map.get(char.lower(), char)
        
        return char
    
    def get_best_reverse_path(self) -> str:
        """Get the best reverse romanization path as a string"""
        best_edges = self.get_best_edges()
        result = ""
        for edge in best_edges:
            result += edge.target
        return result
    
    def get_best_edges(self) -> List[ReverseEdge]:
        """Get the best path through the lattice"""
        # Simple greedy approach - take the longest edge at each position
        result = []
        pos = 0
        
        while pos < self.max_vertex:
            if pos in self.edges and self.edges[pos]:
                # Find the longest edge starting at this position
                best_edge = max(self.edges[pos], key=lambda e: e.end - e.start)
                result.append(best_edge)
                pos = best_edge.end
            else:
                pos += 1
        
        return result
    
    def get_all_edges(self) -> List[ReverseEdge]:
        """Get all edges in the lattice"""
        all_edges = []
        for edges_list in self.edges.values():
            all_edges.extend(edges_list)
        return all_edges

def main():
    """Main entry point for reverse uroman"""
    parser = argparse.ArgumentParser(description="Reverse Uroman - Convert Latin to non-Latin scripts")
    parser.add_argument('input', nargs='?', type=str, help='Latin text to convert')
    parser.add_argument('--script', '-s', type=str, default='Arabic', 
                       help='Target script (Arabic, Devanagari, etc.)')
    parser.add_argument('--format', '-f', type=ReverseRomFormat, default=ReverseRomFormat.STR,
                       choices=list(ReverseRomFormat), help='Output format')
    parser.add_argument('--data_dir', type=Path, help='Data directory')
    parser.add_argument('--version', action='version', version=f'reverse_uroman {__version__}')
    
    args = parser.parse_args()
    
    # Create reverse uroman instance
    reverse_uroman = ReverseUroman(data_dir=args.data_dir)
    
    # Get input text
    if args.input:
        text = args.input
    else:
        text = input("Enter Latin text to convert: ")
    
    # Perform reverse romanization
    try:
        result = reverse_uroman.reverse_romanize_string(
            text, 
            target_script=args.script,
            format=args.format
        )
        print(f"Input: {text}")
        print(f"Output ({args.script}): {result}")
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
