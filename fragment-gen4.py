import streamlit as st
import pandas as pd
import random
import re

class TextGenerator:
    def __init__(self, df):
        first_col = df.columns[0]
        self.texts = df[first_col].dropna().tolist()
        self.special_chars = '™®*@$#&%!?.'  # Moved this up
        self.words = self._extract_words()
        self.symbols = self._extract_symbols()  # Moved before patterns
        self.patterns = self._extract_patterns()
        
    def _extract_words(self):
        # Preserve original case of words
        all_words = []
        for text in self.texts:
            words = re.findall(r'\b\w+\b', text)
            all_words.extend(words)
        return list(set(all_words))
    
    def _extract_patterns(self):
        patterns = []
        for text in self.texts:
            pattern = re.sub(r'\b\w+\b', 'WORD', text)
            if any(c in pattern for c in self.special_chars):
                patterns.append(pattern)
        return list(set(patterns))
    
    def _extract_symbols(self):
        symbols = []
        for text in self.texts:
            symbols.extend(re.findall(r'[^\w\s]', text))
        return list(set(symbols))
    
    def _style_word(self, word):
        styles = [
            lambda x: x,                          # original
            lambda x: x.upper(),                  # ALL CAPS
            lambda x: x.lower(),                  # lowercase
            lambda x: x.title(),                  # Title Case
            lambda x: f"{x}™",                    # with trademark
            lambda x: f"*{x}*",                   # with asterisks
            lambda x: f"{x}-{x}",                 # repeated
            lambda x: f"{x}{random.choice(self.special_chars)}", # with special char
            lambda x: ''.join(random.choice([c.upper(), c.lower()]) for c in x) # mIxEd CaSe
        ]
        return random.choice(styles)(word)
    
    def generate_fragments(self, count=5):
        fragments = []
        for _ in range(count):
            method = random.choice([
                self._generate_pattern_based,
                self._generate_random_combo,
                self._generate_stylized,
                self._generate_symbolic
            ])
            fragment = method()
            fragments.append(fragment)
        return fragments
    
    def _generate_pattern_based(self):
        if self.patterns:
            pattern = random.choice(self.patterns)
            fragment = pattern
            while 'WORD' in fragment:
                fragment = fragment.replace('WORD', self._style_word(random.choice(self.words)), 1)
            return fragment
        return self._generate_random_combo()
    
    def _generate_random_combo(self):
        num_words = random.randint(2, 5)
        words = [self._style_word(random.choice(self.words)) for _ in range(num_words)]
        return ' '.join(words)
    
    def _generate_stylized(self):
        base = self._generate_random_combo()
        styles = [
            lambda x: f"({x})",
            lambda x: f"...{x}...",
            lambda x: f"[{x}]",
            lambda x: f"/{x}/",
            lambda x: f"**{x}**",
            lambda x: x.replace(' ', '_'),
            lambda x: x.replace(' ', '-'),
        ]
        return random.choice(styles)(base)
    
    def _generate_symbolic(self):
        words = [self._style_word(random.choice(self.words)) for _ in range(2)]
        if self.symbols:  # Added check for symbols
            num_symbols = min(3, len(self.symbols))
            symbols = random.sample(self.symbols, num_symbols)
            return f"{words[0]}{random.choice(symbols)}{words[1]}"
        return ' '.join(words)

# Streamlit interface
st.title('Idea Generator')

uploaded_file = st.file_uploader("Choose your CSV file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    generator = TextGenerator(df)
    
    num_fragments = st.slider('Number of ideas to generate:', 1, 10, 5)
    
    if st.button('Generate New Ideas', type="primary"):
        new_fragments = generator.generate_fragments(num_fragments)
        st.text_area(
            "Generated Ideas",
            "\n".join(new_fragments),
            height=300
        )