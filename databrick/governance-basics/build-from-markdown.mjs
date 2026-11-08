// Rebuild the theory-only TeX body from the approved Markdown source.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';

const project = path.dirname(fileURLToPath(import.meta.url));
const source = path.resolve(project, '../databricks-governance-basics.md');
const bundled = createRequire(import.meta.url);
const { marked } = await import(pathToFileURL(bundled.resolve('marked')).href);
const sharp = bundled('sharp');
const markdown = fs.readFileSync(source, 'utf8');
const tokens = marked.lexer(markdown);
const images = path.join(project, 'images');
fs.mkdirSync(images, { recursive: true });
for (const name of ['databricks-logo.svg', 'databricks-logo.png', 'lakehouse-architecture.png', 'unity-catalog-hierarchy.png', 'lakeflow-jobs-example.png', 'unity-catalog-lineage.png', 'sources.json']) {
  fs.copyFileSync(path.resolve(project, '../assets/images', name), path.join(images, name));
}
// Lossless rendering of the supplied SVG logo; the original remains in images/.
await sharp(path.join(images, 'databricks-logo.svg'), { density: 300 })
  .png().toFile(path.join(images, 'databricks-logo-print.png'));

function esc(value) {
  const map = { '\\': '\\textbackslash{}', '{': '\\{', '}': '\\}', '#': '\\#', '$': '\\$', '%': '\\%', '&': '\\&', '_': '\\_', '~': '\\textasciitilde{}', '^': '\\textasciicircum{}', '→': '\\ensuremath{\\rightarrow}', '↓': '\\ensuremath{\\downarrow}', '–': '--', '—': '---', '\u00a0': '~' };
  return String(value).replace(/[\\{}#$%&_~^→↓–—\u00a0]/g, c => map[c]);
}
function code(value) {
  return '\\texttt{' + String(value).split('').map(c => {
    if (c === '_') return '\\_\\allowbreak{}';
    if (c === '.' || c === '/') return c + '\\allowbreak{}';
    return esc(c);
  }).join('') + '}';
}
function inline(list = []) {
  return list.map(t => {
    if (t.type === 'text' || t.type === 'escape') return t.tokens ? inline(t.tokens) : esc(t.text);
    if (t.type === 'strong') return '\\textbf{' + inline(t.tokens) + '}';
    if (t.type === 'em') return '\\emph{' + inline(t.tokens) + '}';
    if (t.type === 'codespan') return code(t.text);
    if (t.type === 'link') {
      if (!/^https?:\/\//i.test(t.href)) return inline(t.tokens);
      return '\\href{' + t.href.replace(/%/g, '\\%').replace(/#/g, '\\#') + '}{' + inline(t.tokens) + '}';
    }
    if (t.type === 'br') return '\\\\';
    throw new Error('Unsupported inline token: ' + t.type);
  }).join('');
}

const overview = String.raw`\begin{tikzpicture}[node distance=10mm]
\node[aivnnode,text width=4.4cm] (w) at (0,0) {\textbf{Workspace}\\Notebook, file, truy vấn};
\node[aivnnode,text width=4.4cm] (j) at (6.4,0) {\textbf{Jobs}\\Task và lịch chạy};
\node[aivnnode,text width=4.4cm] (c) at (3.2,-1.7) {\textbf{Compute}\\Thực thi câu lệnh};
\node[aivnnode,text width=4.4cm] (d) at (3.2,-3.5) {\textbf{Bảng dữ liệu}\\Đọc và ghi};
\node[aivnnode,text width=3.7cm] (u) at (9.2,-3.5) {\textbf{Unity Catalog}\\Namespace, metadata, quyền};
\draw[aivnarrow] (w)--(c); \draw[aivnarrow] (j)--(c);
\draw[aivnarrow] (c)--(d);
\draw[aivnarrow,dashed] (u)--node[above,font=\scriptsize,align=center] {Quản trị\\truy cập} (d);
\end{tikzpicture}`;
const jobs = String.raw`\begin{tikzpicture}[node distance=6mm]
\node[aivnnode,text width=2.65cm] (a) {Nạp\\đơn hàng};
\node[aivnnode,text width=2.65cm,right=of a] (b) {Làm sạch\\dữ liệu};
\node[aivnnode,text width=2.65cm,right=of b] (c) {Tính\\doanh thu};
\node[aivnnode,text width=2.65cm,right=of c] (d) {Kiểm tra\\kết quả};
\draw[aivnarrow] (a)--(b); \draw[aivnarrow] (b)--(c); \draw[aivnarrow] (c)--(d);
\end{tikzpicture}`;
const hierarchy = String.raw`\begin{tikzpicture}[node distance=8mm]
\node[aivnnode,text width=4.7cm] (m) {\textbf{Metastore}};
\node[aivnnode,text width=4.7cm,below=of m] (c) {Catalog: \texttt{lab\_governance}};
\node[aivnnode,text width=3.5cm,below=10mm of c] (s) {Schema: \texttt{silver}};
\node[aivnnode,text width=3.5cm,left=5mm of s] (b) {Schema: \texttt{bronze}};
\node[aivnnode,text width=3.5cm,right=5mm of s] (g) {Schema: \texttt{gold}};
\node[aivnnode,text width=3.5cm,below=of b] (bt) {\texttt{orders\_raw}\\\footnotesize Table};
\node[aivnnode,text width=3.5cm,below=of s] (st) {\texttt{orders\_clean}\\\footnotesize Table};
\node[aivnnode,text width=3.5cm,below=of g] (gt) {\texttt{daily\_sales}\\\footnotesize Table};
\draw[aivnarrow] (m)--(c); \draw[aivnarrow] (c)--(b); \draw[aivnarrow] (c)--(s); \draw[aivnarrow] (c)--(g);
\draw[aivnarrow] (b)--(bt); \draw[aivnarrow] (s)--(st); \draw[aivnarrow] (g)--(gt);
\end{tikzpicture}`;
const lineage = String.raw`\begin{center}
\begin{tikzpicture}[node distance=6mm]
\node[aivnnode,text width=4.15cm,font=\footnotesize] (b) {\texttt{bronze.orders\_raw}\\Dữ liệu gốc};
\node[aivnnode,text width=4.15cm,font=\footnotesize,right=of b] (s) {\texttt{silver.orders\_clean}\\Đơn hợp lệ};
\node[aivnnode,text width=4.15cm,font=\footnotesize,right=of s] (g) {\texttt{gold.daily\_sales}\\Doanh thu theo ngày};
\draw[aivnarrow] (b)--(s); \draw[aivnarrow] (s)--(g);
\end{tikzpicture}
\end{center}
\begin{infobox}{Hai bước biến đổi}
\textbf{Lọc:} giữ đơn đã thanh toán và có số tiền dương.\\
\textbf{Tổng hợp:} tính doanh thu theo ngày.
\end{infobox}`;

let pending = null;
let figureCount = 0;
let tableCount = 0;
let bodyStarted = false;
let bibliography = false;
const output = ['% Generated from the approved theory Markdown; no executable lab included.'];
function figure(graphic, caption) {
  figureCount++;
  return '\\begin{figure}[!htbp]\n\\centering\n' + graphic +
    '\n\\begin{figurecardcaptionaivn}\n\\capfig{' + caption +
    '}\n\\end{figurecardcaptionaivn}\n\\end{figure}\n';
}
function table(t) {
  tableCount++;
  const n = t.header.length;
  let cols = n === 2 ? 'p{0.24\\linewidth}Y' : 'p{0.20\\linewidth}YY';
  if (t.header[0].text === 'Địa chỉ') cols = 'p{0.45\\linewidth}Y';
  if (t.header[0].text === 'Câu') cols = 'p{0.07\\linewidth}Y';
  if (t.header[0].text === 'Quyền') cols = 'p{0.23\\linewidth}p{0.22\\linewidth}Y';
  const row = cells => cells.map(c => inline(c.tokens)).join(' & ') + ' \\\\';
  return '\\begin{table}[H]\n\\small\n\\renewcommand{\\arraystretch}{1.25}\n' +
    '\\begin{tabularx}{\\linewidth}{@{}' + cols + '@{}}\n\\toprule\n' +
    '\\rowcolor{rowLavender}\n' + t.header.map(c => '\\textbf{' + inline(c.tokens) + '}').join(' & ') + ' \\\\\n\\midrule\n' +
    t.rows.map(row).join('\n') + '\n\\bottomrule\n\\end{tabularx}\n\\end{table}\n';
}
for (const t of tokens) {
  if (t.type === 'space') continue;
  if (t.type === 'heading') {
    if (t.depth === 1) continue;
    if (pending) throw new Error('Figure has no caption before heading: ' + t.text);
    if (!bodyStarted) {
      output.push('\\clearpage\n\\tableofcontents\n\\clearpage');
      bodyStarted = true;
    }
    if (t.text === 'Tài liệu tham khảo') {
      bibliography = true;
      output.push('\\FloatBarrier\n\\clearpage\n\\section*{Tài liệu tham khảo}\n\\addcontentsline{toc}{section}{Tài liệu tham khảo}');
      continue;
    }
    const title = t.text.replace(/^\d+(?:\.\d+)*\.\s*/, '');
    const space = title === 'Gợi ý trả lời' ? 18 : 5;
    output.push('\\FloatBarrier\n\\Needspace{' + space + '\\baselineskip}\n\\' + (t.depth === 2 ? 'section' : 'subsection') + '{' + esc(title) + '}');
    continue;
  }
  if (t.type === 'paragraph') {
    if (t.tokens.length === 1 && t.tokens[0].type === 'image') {
      const name = path.basename(t.tokens[0].href);
      if (name === 'databricks-logo.svg') {
        output.push('\\begin{center}\n\\includegraphics[width=5.5cm]{images/databricks-logo-print.png}\n\\end{center}');
      } else pending = '\\includegraphics[width=\\linewidth,height=0.57\\textheight,keepaspectratio]{images/' + name + '}';
      continue;
    }
    if (pending && /^\*Hình \d+\./.test(t.text)) {
      const captionTokens = structuredClone(t.tokens[0].tokens);
      captionTokens[0].text = captionTokens[0].text.replace(/^Hình \d+\.\s*/, '');
      output.push(figure(pending, inline(captionTokens)));
      pending = null;
      continue;
    }
    if (!bodyStarted && /^\*Biểu trưng/.test(t.text)) {
      output.push('\\begin{center}\\scriptsize ' + inline(t.tokens) + '\\end{center}');
      continue;
    }
    if (!bodyStarted && /^\*Từ workspace/.test(t.text)) {
      output.push('\\begin{center}\\large ' + inline(t.tokens) + '\\end{center}');
      continue;
    }
    if (!bodyStarted && /^\*\*Mục tiêu:/.test(t.text)) {
      output.push('\\begin{infobox}{Mục tiêu bài học}\n' + inline(t.tokens).replace(/^\\textbf\{Mục tiêu:\}\s*/, '').replace(/^sau /, 'Sau ') + '\n\\end{infobox}');
      continue;
    }
    output.push(inline(t.tokens) + '\n');
    continue;
  }
  if (t.type === 'blockquote') {
    output.push('\\begin{notebox}\n' + t.tokens.filter(x => x.type === 'paragraph').map(x => inline(x.tokens)).join('\n\n') + '\n\\end{notebox}');
    continue;
  }
  if (t.type === 'table') { output.push(table(t)); continue; }
  if (t.type === 'list') {
    const env = t.ordered ? 'enumerate' : 'itemize';
    output.push((bibliography ? '\\begingroup\\small\n' : '') + '\\begin{' + env + '}\n' +
      t.items.map(item => '\\item ' + item.tokens.filter(x => x.type === 'text' || x.type === 'paragraph').map(x => inline(x.tokens || marked.Lexer.lexInline(x.text))).join(' ')).join('\n') +
      '\n\\end{' + env + '}' + (bibliography ? '\n\\endgroup' : ''));
    continue;
  }
  if (t.type === 'code') {
    if (t.lang === 'mermaid') { pending = t.text.startsWith('flowchart TD') ? overview : jobs; continue; }
    if (t.text.startsWith('Metastore\n')) { pending = hierarchy; continue; }
    if (t.text.startsWith('bronze.orders_raw\n')) { output.push(lineage); continue; }
    if (t.text.startsWith('Ai?')) {
      output.push(String.raw`\begin{examplebox}{Một quyết định cấp quyền}
\begin{tabularx}{\linewidth}{@{}YYY@{}}
\textbf{Ai?} & \textbf{Được làm gì?} & \textbf{Trên tài sản nào?}\\
\texttt{lab\_analysts} & \texttt{SELECT} & \texttt{gold.daily\_sales}
\end{tabularx}
\end{examplebox}`);
      continue;
    }
    const title = t.lang === 'sql' ? (t.text.startsWith('SELECT') ? 'Ví dụ truy vấn bằng tên bảng đầy đủ' : 'Hai phạm vi cấp quyền SELECT') : (t.text.startsWith('/Shared') ? 'Ví dụ tổ chức notebook trong workspace' : 'Tên bảng ba cấp');
    output.push('\\begin{aivncodebox}[language=' + (t.lang === 'sql' ? 'SQL' : '{}') + ']{' + title + '}\n' + t.text + '\n\\end{aivncodebox}');
    continue;
  }
  if (t.type === 'def') continue;
  throw new Error('Unsupported block token: ' + t.type);
}
if (pending) throw new Error('Unfinished figure');
if (figureCount !== 7 || tableCount !== 6) throw new Error(`Unexpected conversion counts: ${figureCount} figures, ${tableCount} tables`);
const content = output.join('\n\n') + '\n';
if (content.includes('CREATE CATALOG lab_governance')) throw new Error('Executable lab leaked into theory');
if (content.includes('\\subsection{Câu hỏi củng cố}') || content.includes('\\subsection{Gợi ý trả lời}')) throw new Error('Quiz content leaked into theory');
fs.writeFileSync(path.join(project, 'content.tex'), content, 'utf8');
console.log(`Theory converted: ${figureCount} numbered figures, ${tableCount} tables; five official image assets included.`);
