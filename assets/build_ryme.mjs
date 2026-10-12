import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import header from './ryme/sleek-header.ts';
import skills from './ryme/sleek-skills.ts';

const root = dirname(fileURLToPath(import.meta.url));
const theme = { bg: '#0d1117', fg: '#f0f6fc', accent: '#67e8f9', muted: '#a5aec0' };
const info = {
  name: 'Nguyen Minh Chanh', role: 'Computer Vision & Multimodal AI',
  org: 'FPT University', location: 'Vietnam', tagline: '', bio: '',
  skills: ['Python', 'PyTorch', 'TensorFlow', 'OpenCV', 'Pandas', 'FastAPI', 'Docker', 'Edge AI'],
  socials: [], githubUsername: 'JayC0603', githubStats: null,
};
let hero = header.renderSvg(info, theme, 8, { loopText: false });
hero = hero.replace('<style>', `<style>
  .underline { animation: accentPulse 5s ease-in-out infinite; }
  .corner { animation: cornerPulse 5s ease-in-out infinite; }
  @keyframes accentPulse { 0%,100% {opacity:.45} 50% {opacity:1;fill:#a78bfa} }
  @keyframes cornerPulse { 0%,100% {opacity:.35} 50% {opacity:.9} }
  @media (prefers-reduced-motion: reduce) { .underline,.corner {animation:none} }
`);
hero = hero.replace('<defs>', '<title>Nguyen Minh Chanh — Computer Vision and Multimodal AI</title><defs>');
writeFileSync(join(root, 'ryme-header.svg'), hero);
writeFileSync(join(root, 'ryme-skills.svg'), skills.renderSvg(info, theme, 8, { loopText: false }));

const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;');
const projects = [
  ['neurix', '01', 'Neurix', 'Multimodal IoT / Edge AI', 'Vision and acoustic analysis for durian quality assessment.', 'Raspberry Pi · PyTorch · ONNX · OpenCV · Librosa', '#67e8f9'],
  ['vehiclevision', '02', 'VehicleVision', 'Computer Vision / Tracking', 'YOLOv8 / YOLO11 detection, attention and augmentation experiments.', 'PyTorch · Ultralytics · OpenCV · Supervision', '#a78bfa'],
  ['voxscribe', '03', 'VoxScribe', 'Speech / Applied AI', 'Speech transcription APIs and notebook-based streaming experiments.', 'FastAPI · Faster Whisper · FFmpeg · Transformers', '#67e8f9'],
];
for (const [id, number, name, label, description, stack, color] of projects) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="150" viewBox="0 0 800 150" role="img" aria-label="${escape(name)} project">
  <title>${escape(name)} — ${escape(label)}</title>
  <rect x="1" y="1" width="798" height="148" rx="14" fill="#0d1117" stroke="#293342"/>
  <rect x="24" y="25" width="3" height="100" rx="1.5" fill="${color}"/>
  <g font-family="Segoe UI, Arial, sans-serif">
  <text x="48" y="37" fill="${color}" font-size="11" letter-spacing="1.2">${number} / ${escape(label.toUpperCase())}</text>
  <text x="48" y="69" fill="#f0f6fc" font-size="25" font-weight="700">${name}</text>
  <text x="48" y="97" fill="#a5aec0" font-size="14">${escape(description)}</text>
  <text x="48" y="124" fill="${color}" font-size="12">${escape(stack)}</text>
  <text x="746" y="70" fill="${color}" font-size="28">↗</text></g></svg>`;
  writeFileSync(join(root, `project-${id}.svg`), svg);
}
console.log('Generated RyMe Sleek header, skills and three matching project cards.');
