import streamlit as st
import pandas as pd
import random
import re

class TextGenerator:
    def __init__(self, df):
        # Get first column of data
        first_col = df.columns[0]
        self.texts = df[first_col].dropna().tolist()
        
        # Build vocabulary from your texts
        self.words = self._extract_words()
        self.patterns = self._extract_patterns()
        
    def _extract_words(self):
        # Extract all unique words from input texts
        all_words = []
        for text in self.texts:
            words = re.findall(r'\b\w+\b', text.upper())
            all_words.extend(words)
        return list(set(all_words))
    
    def _extract_patterns(self):
        # Extract common patterns from input texts
        patterns = []
        for text in self.texts:
            # Keep special characters and spacing patterns
            pattern = re.sub(r'\b\w+\b', 'WORD', text.upper())
            patterns.append(pattern)
        return list(set(patterns))
    
    def generate_fragments(self, count=5):
        fragments = []
        for _ in range(count):
            if random.random() > 0.5:
                # Use pattern-based generation
                pattern = random.choice(self.patterns)
                fragment = pattern
                while 'WORD' in fragment:
                    fragment = fragment.replace('WORD', random.choice(self.words), 1)
            else:
                # Combine random words
                num_words = random.randint(2, 4)
                fragment = ' '.join(random.sample(self.words, num_words))
            
            fragments.append(fragment)
        return fragments

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