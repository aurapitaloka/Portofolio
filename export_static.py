import os
import shutil
import re
import sys

# Ensure current directory is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from app import app, db, Profile

def export_site():
    print("1. Syncing uploads from static/uploads to public/uploads...")
    src_uploads = os.path.join(ROOT_DIR, 'static', 'uploads')
    dst_uploads = os.path.join(ROOT_DIR, 'public', 'uploads')
    
    if os.path.exists(src_uploads):
        os.makedirs(dst_uploads, exist_ok=True)
        for root, dirs, files in os.walk(src_uploads):
            rel_path = os.path.relpath(root, src_uploads)
            target_dir = os.path.join(dst_uploads, rel_path)
            os.makedirs(target_dir, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
        print("   Uploads synced successfully.")
    else:
        print("   Warning: static/uploads not found.")

    print("2. Rendering Flask index template with current database content...")
    with app.app_context():
        client = app.test_client()
        res = client.get('/')
        if res.status_code != 200:
            raise Exception(f"Failed to render index: HTTP {res.status_code}")
        html = res.data.decode('utf-8')

    print("3. Updating contact form fallback for static hosting...")
    # Add smart contact fallback if /api/contact is unavailable (e.g. on Vercel static)
    fallback_js = """
        try {
          const res = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (!res.ok) throw new Error("Static / serverless host");
          const result = await res.json();
          contactAlert.classList.remove('hidden');
          if (result.success) {
            contactAlert.className = "p-3.5 rounded-xl text-xs font-semibold bg-emerald-950/60 text-emerald-300 border border-emerald-800";
            contactAlert.innerHTML = '<i class="fas fa-circle-check mr-1.5"></i>' + result.message;
            contactForm.reset();
          } else {
            contactAlert.className = "p-3.5 rounded-xl text-xs font-semibold bg-rose-950/60 text-rose-300 border border-rose-800";
            contactAlert.innerHTML = '<i class="fas fa-circle-exclamation mr-1.5"></i>' + result.message;
          }
        } catch (err) {
          // Fallback for static hosting (Vercel)
          contactAlert.classList.remove('hidden');
          const mailto = `mailto:aurapitaloka04@gmail.com?subject=${encodeURIComponent(payload.subject || 'Pesan dari Portofolio')}&body=${encodeURIComponent('Nama: ' + payload.name + '\\nEmail: ' + payload.email + '\\n\\nPesan:\\n' + payload.message)}`;
          window.open(mailto, '_blank');
          contactAlert.className = "p-3.5 rounded-xl text-xs font-semibold bg-emerald-950/60 text-emerald-300 border border-emerald-800";
          contactAlert.innerHTML = '<i class="fas fa-circle-check mr-1.5"></i>Terima kasih! Pesan Anda telah disiapkan via email (aurapitaloka04@gmail.com).';
          contactForm.reset();
        }
    """
    
    # Replace the fetch block in HTML
    pattern = re.compile(r'try\s*\{\s*const res = await fetch\(\'/api/contact\'.*?catch\s*\(err\)\s*\{.*?\}\s*finally', re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(fallback_js + "\n        finally", html)
        print("   Contact form fallback injected.")

    print("4. Writing updated index.html...")
    target_index = os.path.join(ROOT_DIR, 'index.html')
    with open(target_index, 'w', encoding='utf-8') as f:
        f.write(html)
    print("   index.html written successfully.")

if __name__ == '__main__':
    export_site()
