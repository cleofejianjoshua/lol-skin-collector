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

export function useSound() {
  const sounds = {
    pipSound:    makeSound('/sounds/sound_pip.mp3',    0.2),
    pullSound:   makeSound('/sounds/sound_select.mp3', 0.4),
    revealSound: makeSound('/sounds/sound_open.mp3',  0.35),
    clickSound:  makeSound('/sounds/sound_click.mp3',  0.5),
    goldSound:   makeSound('/sounds/sound_gold.mp3',  0.2),
  };

  return sounds;
}