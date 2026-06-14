import hashlib
import sqlite3
import os

def chunk_text(text, chunk_size=1200, overlap=150):
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunks.append(text[start:end])
        start+=(chunk_size-overlap)
    return chunks
def generate_text_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()
def build_grounded_prompt(context_chunks, task_type='summary'):
    combined_context="\n---CONTEXT SEPARATOR ---\n".join(context_chunks)
    if task_type=='summary':
        system_ins=(
            "you are an academic verfication assisistant. your absolute rule is to summarize the text provided below.\n"
            "ANTI-HALLUCINATION SAFEGUARDS :\n"
            "1. reply only on the facts explicitly mentioned in the source material.\n"
            "2. do not extrapolate,interpret or introduce outside world facts or assumptions.\n"
            "3. if a concept cannot be verified directly from the text ,omit it entirely." 
        )
    else:
        system_ins=(
            "you are a factual quiz generation engine.generate a comprehensive study quiz based on the text below\n"
            "ANTI-HALLUCINATION SAFEGUARDS :\n"
            "1. Every question and current answer choice must correspond directly to  a sentence in the context.\n6"
            "2.do not include external logic puzzles or external textbook facts not found in this document.6"
        )
    prompt=f"""
{system_ins}
---start of verified source material---
{combined_context}
---end of verified source material---
please execute the request adhering strictly to the anti-hallucination safegaurds above:
"""
    return prompt

DB_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'eduai_valut.db')
def save_documnet_to_db(filename,raw_text):
    try:
        conn=sqlite3.connect(DB_path)
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM documents WHERE filename=?",(filename,))
        exists=cursor.fetchone()
        if not exists:
            cursor.execute("INSERT INTO documents (filename, processed_text)VALUES (?,?)",(filename,raw_text))
            conn.commit()
            print(f"Document '{filename}' saved to database.")
        else:
            print(f"Document '{filename}' already exists in the database.")
        conn.close()
    except Exception as e:
        print(f"Error saving document to database: {e}")
def check_cache(text_hash,request_type):
        conn=sqlite3.connect(DB_path)
        cursor=conn.cursor()
        cursor.execute("SELECT cached_response FROM response_cache WHERE text_hash=? AND request_type=?",(text_hash,request_type))
        result=cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
def save_to_cache(text_hash,request_type,response_text):
        try:
            conn=sqlite3.connect(DB_path)
            cursor=conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO response_cache (text_hash, request_type, cached_response) VALUES (?,?,?)",(text_hash,request_type,response_text))
            conn.commit()
            conn.close()
            print("response cached cleanly.")
        except Exception as e:
            print(f"Error saving to cache: {e}")    