// Import CSS
import './input.css'

// Portfolio JavaScript

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    const icon = mobileMenuBtn.querySelector('i');
    if (icon) {
      icon.classList.toggle('fa-bars');
      icon.classList.toggle('fa-times');
    }
  });
}

// Smooth scroll untuk navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
      // Close mobile menu jika terbuka
      if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    }
  });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('nav');

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll > 100) {
    navbar.classList.add('shadow-lg');
  } else {
    navbar.classList.remove('shadow-lg');
  }
  
  lastScroll = currentScroll;
});

// Active nav link on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function highlightNav() {
  const scrollY = window.pageYOffset;

  sections.forEach(section => {
    const sectionHeight = section.offsetHeight;
    const sectionTop = section.offsetTop - 100;
    const sectionId = section.getAttribute('id');

    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
      navLinks.forEach(link => {
        link.classList.remove('text-primary');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('text-primary');
        }
      });
    }
  });
}

window.addEventListener('scroll', highlightNav);

// Experience Tabs
const experienceTabs = document.querySelectorAll('.experience-tab');
const experienceContents = document.querySelectorAll('.experience-content');

experienceTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const targetTab = tab.getAttribute('data-tab');
    
    // Remove active class from all tabs
    experienceTabs.forEach(t => {
      t.classList.remove('active', 'bg-primary', 'text-white');
      t.classList.add('bg-slate-800', 'text-gray-300');
    });
    
    // Add active class to clicked tab
    tab.classList.add('active', 'bg-primary', 'text-white');
    tab.classList.remove('bg-slate-800', 'text-gray-300');
    
    // Hide all contents
    experienceContents.forEach(content => {
      content.classList.add('hidden');
    });
    
    // Show target content
    const targetContent = document.getElementById(`${targetTab}-content`);
    if (targetContent) {
      targetContent.classList.remove('hidden');
    }
  });
});

// Form submission dengan EmailJS
const contactForm = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const submitText = document.getElementById('submit-text');
const formMessage = document.getElementById('form-message');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Disable button
    submitBtn.disabled = true;
    submitText.textContent = 'Mengirim...';
    
    // Simulasi pengiriman (ganti dengan EmailJS jika sudah setup)
    // Untuk sementara, kita simpan ke localStorage sebagai backup
    const formData = {
      name,
      email,
      message,
      timestamp: new Date().toISOString()
    };
    
    // Simpan ke localStorage (untuk testing)
    const savedMessages = JSON.parse(localStorage.getItem('contactMessages') || '[]');
    savedMessages.push(formData);
    localStorage.setItem('contactMessages', JSON.stringify(savedMessages));
    
    // Tampilkan pesan sukses
    formMessage.classList.remove('hidden');
    formMessage.classList.add('text-green-400');
    formMessage.innerHTML = '<i class="fas fa-check-circle mr-2"></i>Pesan berhasil dikirim! Saya akan membalas segera.';
    
    // Reset form
    contactForm.reset();
    
    // Re-enable button setelah 3 detik
    setTimeout(() => {
      submitBtn.disabled = false;
      submitText.textContent = 'Kirim Pesan';
      formMessage.classList.add('hidden');
    }, 3000);
    
    // UNTUK SETUP EMAILJS (Opsional):
    // 1. Daftar di https://www.emailjs.com (gratis)
    // 2. Dapatkan Public Key, Service ID, dan Template ID
    // 3. Uncomment kode di bawah dan isi dengan data Anda:
    /*
    try {
      await emailjs.send(
        'YOUR_SERVICE_ID',      // Ganti dengan Service ID Anda
        'YOUR_TEMPLATE_ID',     // Ganti dengan Template ID Anda
        {
          from_name: name,
          from_email: email,
          message: message
        },
        'YOUR_PUBLIC_KEY'       // Ganti dengan Public Key Anda
      );
      
      formMessage.classList.remove('hidden');
      formMessage.classList.add('text-green-400');
      formMessage.innerHTML = '<i class="fas fa-check-circle mr-2"></i>Pesan berhasil dikirim!';
      contactForm.reset();
    } catch (error) {
      formMessage.classList.remove('hidden');
      formMessage.classList.add('text-red-400');
      formMessage.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>Gagal mengirim pesan. Silakan coba lagi.';
    } finally {
      submitBtn.disabled = false;
      submitText.textContent = 'Kirim Pesan';
    }
    */
  });
}

console.log('Portfolio website loaded!');
