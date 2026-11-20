import os

with open(r'C:\Users\Dell\AppData\Local\Temp\banner_b64.txt', 'r', encoding='ascii') as f:
    b64_banner = f.read().strip()

with open(r'C:\Users\Dell\AppData\Local\Temp\dp_b64.txt', 'r', encoding='ascii') as f:
    b64_dp = f.read().strip()

def make_script(b64, filename, input_idx):
    return f"""() => {{
  const b64Data = '{b64}';
  const byteCharacters = atob(b64Data);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {{
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }}
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], {{ type: 'image/png' }});
  const file = new File([blob], '{filename}', {{ type: 'image/png' }});
  
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  
  const inputs = Array.from(document.querySelectorAll('input[type="file"]'));
  if (inputs[{input_idx}]) {{
    inputs[{input_idx}].files = dataTransfer.files;
    inputs[{input_idx}].dispatchEvent(new Event('change', {{ bubbles: true }}));
    return 'Dispatched change event on input {input_idx} with file: ' + file.name + ' size: ' + file.size;
  }}
  return 'Input {input_idx} not found';
}}"""

with open(r'C:\Users\Dell\AppData\Local\Temp\upload_banner.js', 'w', encoding='utf-8') as f:
    f.write(make_script(b64_banner, '02_WhatsApp_Cover_Banner.png', 0))

with open(r'C:\Users\Dell\AppData\Local\Temp\upload_dp.js', 'w', encoding='utf-8') as f:
    f.write(make_script(b64_dp, '01_WhatsApp_Profile_Picture.png', 1))

print("Both upload scripts generated successfully!")
