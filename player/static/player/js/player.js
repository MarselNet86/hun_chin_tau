/**
 * HunChinTau - Player JavaScript
 * Plyr initialization, hotkeys, episode navigation
 */

let player = null;

// Информация о источнике плеера (передаётся из Django template)
// const player_source = { player_type: 'video' };

document.addEventListener('DOMContentLoaded', function() {
  // Инициализация Plyr (для прямого видео)
  if (typeof window.playerSourceType !== 'undefined' && window.playerSourceType === 'video') {
    const videoElement = document.getElementById('player');
    if (videoElement) {
      player = new Plyr(videoElement, {
        controls: [
          'play-large',
          'play',
          'progress',
          'current-time',
          'mute',
          'volume',
          'captions',
          'settings',
          'pip',
          'airplay',
          'fullscreen'
        ],
        settings: ['captions', 'quality', 'speed'],
        speed: { selected: 1, options: [0.5, 0.75, 1, 1.25, 1.5, 2] }
      });

      // Обработка клавиш для перемотки
      document.addEventListener('keydown', function(e) {
        if (!player || player.duration === Infinity || !player.duration) return;

        // Пробел - пауза/воспроизведение
        if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
          e.preventDefault();
          if (player.playing) {
            player.pause();
          } else {
            player.play();
          }
        }

        // Стрелки - перемотка
        if (e.code === 'ArrowLeft') {
          e.preventDefault();
          player.currentTime = Math.max(0, player.currentTime - 10);
        }
        if (e.code === 'ArrowRight') {
          e.preventDefault();
          player.currentTime = Math.min(player.duration, player.currentTime + 10);
        }

        // Цифры - перемотка на процент
        if (e.key >= '0' && e.key <= '9' && e.target.tagName !== 'INPUT') {
          e.preventDefault();
          const percent = parseInt(e.key) / 10;
          player.currentTime = player.duration * percent;
        }
      });
    }
  }
});

// Навигация между эпизодами
function nextEpisode() {
  const nextUrl = window.nextEpisodeUrl;
  if (nextUrl) {
    window.location.href = nextUrl;
  }
}

function prevEpisode() {
  const prevUrl = window.prevEpisodeUrl;
  if (prevUrl) {
    window.location.href = prevUrl;
  }
}
