function makeSound(src, volume = 0.5) {
  const sound = typeof Audio !== 'undefined' ? new Audio(src) : null;
  if (sound) sound.volume = volume;
  return {
    play() {
      if (!sound) return;
      sound.currentTime = 0;
      sound.play().catch(() => {});
    }
  };
}

function makePool(src, volume = 0.5, size = 8) {
  if (typeof Audio === 'undefined') return { play() {} };
  const pool = Array.from({ length: size }, () => {
    const a = new Audio(src);
    a.volume = volume;
    return a;
  });
  let idx = 0;
  return {
    play() {
      const sound = pool[idx % size];
      idx++;
      sound.currentTime = 0;
      sound.play().catch(() => {});
    }
  };
}

const sounds = {
  pipSound:    makePool('/sounds/sound_pip.mp3',    0.2, 8),
  pullSound:   makeSound('/sounds/sound_select.mp3', 0.4),
  revealSound: makeSound('/sounds/sound_open.mp3',   0.35),
  clickSound:  makeSound('/sounds/sound_click.mp3',  0.5),
  goldSound:   makeSound('/sounds/sound_gold.mp3',   0.2),
};

export function useSound() {
  return sounds;
}