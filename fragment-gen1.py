import streamlit as st
import pandas as pd
import random
import re
from datetime import datetime

class TextGenerator:
    def __init__(self, df):
        first_col = df.columns[0]
        self.texts = df[first_col].dropna().tolist()
        random.shuffle(self.texts)
        self.vocabulary = self._build_vocabulary()
        
    def _build_vocabulary(self):
        # Categorize phrases by type
        violent_phrases = [t for t in self.texts if any(word in t.lower() for word in ['blood', 'kill', 'dead', 'death', 'knife', 'gun'])]
        tech_phrases = [t for t in self.texts if any(char in t for char in ['@', '/', '\\', '#', '*'])]
        emotional_phrases = [t for t in self.texts if any(word in t.lower() for word in ['love', 'hate', 'feel', 'want', 'need'])]
        
        # Collect special characters and symbols
        symbols = []
        for text in self.texts:
            symbols.extend(re.findall(r'[^\w\s]', text))
            
        return {
            'violent': violent_phrases,
            'tech': tech_phrases,
            'emotional': emotional_phrases,
            'symbols': list(set(symbols)),
            'phrases': self.texts
        }
    
    def generate_fragments(self, count=10):
        fragments = []
        used_phrases = set()
        
        generation_methods = [
            self._generate_violent_tech,
            self._generate_emotional_outburst,
            self._generate_broken_english,
            self._generate_corporate_parody,
            self._generate_tech_gibberish,
            self._generate_body_humor
        ]
        
        for _ in range(count):
            method = random.choice(generation_methods)
            while True:
                fragment = method()
                if fragment not in used_phrases:
                    used_phrases.add(fragment)
                    fragments.append(fragment)
                    break
                
        return fragments
    
    def _generate_violent_tech(self):
        # Combine violence with tech jargon
        tech_symbols = ['@', '#', '/', '\\', '*', '&']
        violent_words = ['KILL', 'DESTROY', 'OBLITERATE', 'SMASH', 'CRUSH']
        tech_words = ['SYSTEM', 'PROTOCOL', 'RUNTIME', 'MEMORY', 'DATABASE']
        
        if random.random() > 0.5:
            return f"{random.choice(violent_words)}{random.choice(tech_symbols)}{random.choice(tech_words)}"
        else:
            return f"({random.choice(violent_words)}.exe has stopped responding)"
    
    def _generate_emotional_outburst(self):
        # Emotional statements with weird formatting
        emotions = ['LOVE', 'HATE', 'NEED', 'WANT', 'CRAVE']
        objects = ['BRAIN', 'SYSTEM', 'REALITY', 'EXISTENCE', 'VOID']
        
        template = random.choice([
            "{}ing your {}...",
            "*{} {} intensifies*",
            "cannot {} enough {}",
            "{} {} until death"
        ])
        return template.format(random.choice(emotions), random.choice(objects))
    
    def _generate_broken_english(self):
        # Deliberately broken/weird English
        base = random.choice(self.texts)
        words = base.split()
        if len(words) > 2:
            words.insert(random.randint(0, len(words)), "... um...")
        return ' '.join(words)
    
    def _generate_corporate_parody(self):
        # Corporate speak gone wrong
        corps = ['MEGACORP', 'BRAINTECH', 'MINDCO', 'THOUGHTWARE']
        products = ['BRAIN', 'MIND', 'SOUL', 'REALITY']
        
        template = random.choice([
            "{}™ - Now with more {}!",
            "NEW from {}: {} 2.0",
            "{}'s Patent-Pending {}",
            "9/10 {} Users Prefer New {}"
        ])
        return template.format(
            random.choice(corps),
            random.choice(products)
        )
    
    def _generate_tech_gibberish(self):
        # Technical nonsense
        prefixes = ['SYS', 'MIND', 'BRAIN', 'SOUL']
        symbols = ['@', '#', '/', '\\', '*', '&', '$']
        suffixes = ['exe', 'dll', 'sys', 'bin']
        
        return f"{random.choice(prefixes)}{random.choice(symbols)}{random.choice(prefixes)}.{random.choice(suffixes)}"
    
    def _generate_body_humor(self):
        # Body-related absurdist humor
        body_parts = ['BRAIN', 'HEAD', 'FACE', 'BODY', 'SKULL']
        actions = ['MELT', 'EXPLODE', 'DISSOLVE', 'TRANSCEND', 'VAPORIZE']
        
        if random.random() > 0.5:
            return f"WARNING: {random.choice(body_parts)} WILL {random.choice(actions)}"
        else:
            return f"({random.choice(body_parts)} status: {random.choice(actions)}D)"

# Streamlit interface
st.set_page_config(page_title="Fragment Generator", layout="wide")
st.title('Fragment Generator')

if 'fragments' not in st.session_state:
    st.session_state.fragments = []
if 'combined_text' not in st.session_state:
    st.session_state.combined_text = ""

uploaded_file = st.file_uploader("Choose your CSV file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    generator = TextGenerator(df)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        num_fragments = st.slider('Number of fragments to generate:', 1, 10, 5)
        
        if st.button('Generate New Fragments', type="primary"):
            new_fragments = generator.generate_fragments(num_fragments)
            new_text = "\n".join(new_fragments)
            st.session_state.combined_text = new_text + (
                "\n" + st.session_state.combined_text if st.session_state.combined_text else ""
            )
        
        st.text_area(
            "Generated Fragments",
            st.session_state.combined_text,
            height=400
        )
        
        if st.session_state.combined_text:
            st.download_button(
                'Download fragments',
                st.session_state.combined_text,
                file_name='fragments.txt'
            )
    
    with col2:
        st.subheader(f'Source Material ({len(generator.texts)} texts)')
        source_text = "\n".join(generator.texts)
        st.text_area("Original texts", source_text, height=600)