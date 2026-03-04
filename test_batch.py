import os
import subprocess
import json

def test_compress_pdfs():
    pdfs_dir = os.path.join(os.path.dirname(__file__), "pdfs")
    
    if not os.path.exists(pdfs_dir):
        print(f"Error: Directory '{pdfs_dir}' does not exist.")
        return
        
    pdf_files = [f for f in os.listdir(pdfs_dir) if f.lower().endswith('.pdf') and not "compressed_" in f]
    
    if not pdf_files:
        print(f"No original PDF files found in '{pdfs_dir}'.")
        return
        
    print(f"Found {len(pdf_files)} PDF files to test in '{pdfs_dir}':")
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdfs_dir, pdf_file)
        print(f"\n{'-'*40}")
        print(f"Testing compression on: {pdf_file}")
        
        # Build command to test the skill via uv run
        cmd = [
            "uv", "run", "src/main.py",
            "--pdf_path", pdf_path,
            "--compression_level", "2"
        ]
        
        try:
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # The result output should be the JSON string emitted by the skill
            stdout_output = result.stdout.strip()
            
            try:
                response = json.loads(stdout_output)
                if response.get("status") == "success":
                    data = response.get("data", {})
                    original_size = data.get("original_size", 0)
                    compressed_size = data.get("compressed_size", 0)
                    ratio = (1 - (compressed_size / original_size)) * 100 if original_size else 0
                    
                    print(f"✅ Success!")
                    print(f"   Original Size:   {original_size / 1024 / 1024:.2f} MB")
                    print(f"   Compressed Size: {compressed_size / 1024 / 1024:.2f} MB")
                    print(f"   Compression Ratio: {ratio:.1f}% reduction")
                    print(f"   Output saved to: {data.get('output_path')}")
                else:
                    print(f"❌ Skill returned error status: {response.get('message')}")
            except json.JSONDecodeError:
                print(f"❌ Failed to parse JSON output. Raw output:\n{stdout_output}")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Execution failed with return code {e.returncode}.")
            print(f"Stderr: {e.stderr}")

if __name__ == "__main__":
    test_compress_pdfs()
