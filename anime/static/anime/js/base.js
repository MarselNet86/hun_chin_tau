/**
 * HunChinTau - Base JavaScript
 * Three.js particles, snow effect, modal, search
 */

(function() {
  // ===== Three.js Particles Background =====
  const canvas = document.getElementById('three-canvas');
  if (!canvas) return;
  
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
  camera.position.z = 400;
  
  const count = 800;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  
  for (let i = 0; i < count; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 2000;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 2000;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 800;
    
    const isRed = Math.random() < 0.12;
    if (isRed) {
      colors[i * 3] = 0.9;
      colors[i * 3 + 1] = 0.0;
      colors[i * 3 + 2] = 0.15;
    } else {
      const b = 0.3 + Math.random() * 0.5;
      colors[i * 3] = b;
      colors[i * 3 + 1] = b;
      colors[i * 3 + 2] = b + 0.1;
    }
    
    sizes[i] = Math.random() * 2.5 + 0.5;
  }
  
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  
  const material = new THREE.PointsMaterial({
    size: 1.8,
    vertexColors: true,
    transparent: true,
    opacity: 0.55,
    sizeAttenuation: true,
  });
  
  const particles = new THREE.Points(geometry, material);
  scene.add(particles);
  
  let t = 0;
  function animate() {
    requestAnimationFrame(animate);
    t += 0.0004;
    particles.rotation.y = t * 0.12;
    particles.rotation.x = t * 0.04;
    
    const pos = geometry.attributes.position.array;
    for (let i = 1; i < count * 3; i += 3) {
      pos[i] -= 0.08;
      if (pos[i] < -1000) pos[i] = 1000;
    }
    geometry.attributes.position.needsUpdate = true;
    
    renderer.render(scene, camera);
  }
  animate();
  
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();

(function() {
  // ===== Snow Effect =====
  const snow = document.getElementById('snow');
  if (!snow) return;
  
  const flakes = ['❄', '❅', '❆', '*'];
  for (let i = 0; i < 28; i++) {
    const f = document.createElement('div');
    f.className = 'flake';
    f.textContent = flakes[Math.floor(Math.random() * flakes.length)];
    f.style.left = Math.random() * 100 + 'vw';
    f.style.top = Math.random() * 100 + 'vh';
    f.style.fontSize = (8 + Math.random() * 10) + 'px';
    f.style.animationDuration = (8 + Math.random() * 18) + 's';
    f.style.animationDelay = (Math.random() * 12) + 's';
    f.style.opacity = 0.2 + Math.random() * 0.4;
    snow.appendChild(f);
  }
})();

// ===== Modal Functions =====
function openModal(anime) {
  const modalImg = document.getElementById('modalImg');
  const modalTitle = document.getElementById('modalTitle');
  const modalRating = document.getElementById('modalRating');
  const modalYear = document.getElementById('modalYear');
  const modalDesc = document.getElementById('modalDesc');
  const modalGenres = document.getElementById('modalGenres');
  const modalWatchBtn = document.getElementById('modalWatchBtn');
  const modalBackdrop = document.getElementById('modalBackdrop');
  
  if (!modalBackdrop) return;
  
  if (modalImg) modalImg.src = anime.img;
  if (modalTitle) modalTitle.textContent = anime.title;
  if (modalRating) modalRating.textContent = anime.rating;
  if (modalYear) modalYear.textContent = anime.year;
  if (modalDesc) modalDesc.textContent = anime.desc;
  if (modalGenres) {
    modalGenres.innerHTML = anime.genres.map(g => '<span class="genre-tag">' + g + '</span>').join('');
  }
  if (modalWatchBtn) {
    modalWatchBtn.onclick = function() {
      window.location.href = '/player/' + anime.id + '/';
    };
  }
  
  modalBackdrop.classList.add('active');
}

function closeModal() {
  const modalBackdrop = document.getElementById('modalBackdrop');
  if (modalBackdrop) {
    modalBackdrop.classList.remove('active');
  }
}

// Close modal on backdrop click
(function() {
  const modalBackdrop = document.getElementById('modalBackdrop');
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });
  }
})();

// ===== Search Functionality =====
(function() {
  const searchBtn = document.getElementById('searchBtn');
  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  let searchTimeout = null;

  if (searchBtn) {
    searchBtn.addEventListener('click', function() {
      if (searchOverlay) {
        searchOverlay.classList.add('active');
      }
      if (searchInput) {
        searchInput.focus();
      }
    });
  }

  if (searchOverlay) {
    searchOverlay.addEventListener('click', function(e) {
      if (e.target === this) {
        searchOverlay.classList.remove('active');
      }
    });
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      if (searchOverlay) searchOverlay.classList.remove('active');
      closeModal();
    }
  });

  // Search with debounce
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      
      clearTimeout(searchTimeout);
      
      if (query.length < 2) {
        if (searchResults) searchResults.innerHTML = '';
        return;
      }

      searchTimeout = setTimeout(function() {
        if (searchResults) {
          searchResults.innerHTML = '<div class="search-loading"><div class="loading-spinner"></div></div>';
        }
        
        fetch('/search/?q=' + encodeURIComponent(query))
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
          })
          .then(data => {
            if (!searchResults) return;
            
            if (data.results && data.results.length > 0) {
              searchResults.innerHTML = data.results.map(anime => `
                <div class="search-result-item" onclick="window.location.href='/anime/${anime.slug}/'">
                  <img src="${anime.poster}" alt="${anime.title}" class="search-result-img" loading="lazy"/>
                  <div class="search-result-info">
                    <div class="search-result-title">${anime.title}</div>
                    <div class="search-result-desc">${anime.description}</div>
                    <div class="search-result-meta">
                      <span class="search-result-score">★ ${anime.score}</span>
                      <span>${anime.year}</span>
                    </div>
                    <button class="search-result-btn" onclick="event.stopPropagation(); window.location.href='/player/${anime.id}/'">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                      Смотреть
                    </button>
                  </div>
                </div>
              `).join('');
            } else if (data.results && data.results.length === 0) {
              searchResults.innerHTML = '<div class="search-no-results">Такого аниме пока нет</div>';
            }
          })
          .catch(error => {
            if (searchResults) {
              searchResults.innerHTML = '<div class="search-no-results">Ошибка поиска. Попробуйте позже.</div>';
            }
          });
      }, 300);
    });
  }
})();
