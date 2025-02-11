import anthropic
import re
import os

client = None

def init_client(api_key):
   global client
   client = anthropic.Anthropic(api_key=api_key)

def generate_response(query):
   global client
   message = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=1024,
      messages=[
         {
               "role":"system",
               "content": "You are expert flowchart creator. You need to design flowcharts using mermaid.js. Output the flowchart in markdown format",
               "role": "user",
               "content": f"Create a flowchart based on given scenario:{query}"
         }
      ]
   )
   return message.content[0].text

def generate_response_steps(steps):
   
   global client
   message = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=1024,
      messages=[
         {
               "role":"system",
               "content": "You are expert flowchart creator. You need to design flowcharts using mermaid.js. Output the flowchart in markdown format from user inputs only. Do not add any explanation",
               "role": "user",
               "content": f"Create a flowchart from these steps:{steps}"
         }
      ]
   )
   return message.content[0].text

def process_query(query):
   response = generate_response(query)
   code_pattern = r"```mermaid\n(.*?)```"
   text_pattern = r"```mermaid.*?```\n(.*)"
   mermaid = re.search(pattern=code_pattern, string=response, flags=re.DOTALL).group(1)
   explanation = re.search(pattern=text_pattern, string=response, flags=re.DOTALL).group(1)
   return mermaid, explanation
  
def html_code(code):
   # HTML to render the Mermaid diagram
      html_code = f"""
      <div class="mermaid">
         {code}
      </div>
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <script>
         mermaid.initialize({{ startOnLoad: true }});
      </script>
      """
      return html_code
   
def custom_code(theme, mermaid_code):
   if theme.lower() == "forest":
      return """%%{init: {'theme': 'forest'}}%%""" + f"""{mermaid_code}"""
   elif theme.lower() == "dark":
      return """%%{init: {'theme': 'dark'}}%%""" + f"""{mermaid_code}"""
   else:
      return mermaid_code
   
def process_steps_query(steps):
   response = generate_response_steps(steps)
   code_pattern = r"```mermaid\n(.*?)```"
   text_pattern = r"```mermaid.*?```\n(.*)"
   mermaid = re.search(pattern=code_pattern, string=response, flags=re.DOTALL).group(1)
   return mermaid

def htmlWrapper(mermaidCode):
   # Wrapper HTML with a script to dynamically resize the iframe
   html_code = f"""
   <!DOCTYPE html>
   <html>
   <head>
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <style>
         body {{
               margin: 0;
               padding: 0;
         }}
      </style>
   </head>
   <body>
      <div id="container">
         {mermaidCode}
      </div>
      <script>
         // Function to resize iframe dynamically
         const resizeObserver = new ResizeObserver(entries => {{
               for (let entry of entries) {{
                  const height = entry.contentRect.height;
                  window.parent.postMessage({{ height }}, "*");
               }}
         }});
         resizeObserver.observe(document.getElementById('container'));
      </script>
   </body>
   </html>
   """
   return html_code
   
# Function to simulate the download process
def processDownload(mermaid,filename, extension):
    htmlCode = htmlWrapper(mermaid)  # Generate HTML
    # Define the localhost server's directory (e.g., 'localhost_files')
    server_directory = os.path.join(os.getcwd(), "static")
    os.makedirs(server_directory, exist_ok=True)  # Create directory if it doesn't exist
    # Save the file
    file_path = os.path.join(server_directory, f"{filename}.{extension}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(htmlCode)
    # Return localhost URL
    localhost_url = f"/static/{filename}.{extension}"
    return localhost_url