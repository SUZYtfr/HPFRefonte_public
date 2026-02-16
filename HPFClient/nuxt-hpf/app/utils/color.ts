function hexToRgb(hexColor: string): [number, number, number] | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexColor);
  if (result != null) {
    const r = parseInt(result[1]!, 16);
    const g = parseInt(result[2]!, 16);
    const b = parseInt(result[3]!, 16);
    return [r, g, b];
  }
  return null;
}

function rgbToHsl(r: number, g: number, b: number): [number, number, number] {
  r /= 255;
  g /= 255;
  b /= 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s;
  const l = (max + min) / 2;

  if (max === min) {
    h = s = 0; // achromatic
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      case b:
        h = (r - g) / d + 4;
        break;
    }
    h /= 6;
  }

  return [h * 360, s * 100, l * 100];
}

function hexToHsl(hexColor: string): [number, number, number] | null {
  const t = hexToRgb(hexColor);
  if (t != null) return rgbToHsl(t[0], t[1], t[2]);
  return null;
}

function invertHex(hexColor: string): string {
  if (hexColor.startsWith("#")) hexColor = hexColor.substring(1);
  return "#" + (Number(`0x1${hexColor}`) ^ 0xffffff).toString(16).substring(1).toUpperCase();
}

export { rgbToHsl, hexToRgb, hexToHsl, invertHex };
