import cairo
import zipfile
import xml.etree.ElementTree as ET
import statistics
import os
import math

# 1. Parse Excel data
with zipfile.ZipFile('Pesquisa sobre Desenvolvimento Front-End_ JavaScript vs TypeScript (respostas) (1).xlsx', 'r') as z:
    shared_strings = []
    ss_root = ET.fromstring(z.read('xl/sharedStrings.xml'))
    for si in ss_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
        texts = [t.text for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t') if t.text]
        shared_strings.append(''.join(texts))
    
    sheet_root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    header = {}
    data = []
    
    for r_idx, row in enumerate(sheet_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')):
        row_dict = {}
        for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
            r_ref = c.attrib.get('r')
            col_letters = ''.join([ch for ch in r_ref if ch.isalpha()])
            t = c.attrib.get('t')
            v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            val = v.text if v is not None else None
            if t == 's' and val is not None:
                val = shared_strings[int(val)]
            row_dict[col_letters] = val
        if r_idx == 0:
            header = row_dict
        else:
            data.append(row_dict)

total_n = len(data)
g_inic = [d for d in data if d['B'] in ['Menos de 1 ano', '1 a 3 anos']] # N=14
g_exp = [d for d in data if d['B'] in ['4 a 6 anos', '7 a 10 anos', 'Mais de 10 anos']] # N=9

os.makedirs('04-figuras', exist_ok=True)

# Helper function for drawing rounded rectangles
def round_rect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

# Font helper
def draw_text(ctx, text, x, y, size=14, bold=False, color=(0.1, 0.1, 0.1), align='left'):
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ctx.set_source_rgb(*color)
    ext = ctx.text_extents(text)
    if align == 'center':
        x -= ext.width / 2 + ext.x_bearing
    elif align == 'right':
        x -= ext.width + ext.x_bearing
    ctx.move_to(x, y)
    ctx.show_text(text)
    return ext

# -------------------------------------------------------------
# FIGURA 1: Demografia e Experiência
# -------------------------------------------------------------
def generate_fig1():
    w, h = 1400, 750
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Title & Subtitle
    draw_text(ctx, "Perfil dos Respondentes: Experiência e Escala de Projetos", 50, 50, size=24, bold=True, color=(0.08, 0.18, 0.36))
    draw_text(ctx, f"Amostra total: N = {total_n} desenvolvedores front-end", 50, 80, size=15, bold=False, color=(0.4, 0.45, 0.5))

    # Panel 1: Tempo de Experiência (Bar chart)
    draw_text(ctx, "A. Tempo de Experiência no Front-End", 60, 130, size=18, bold=True, color=(0.15, 0.25, 0.45))
    
    exp_cats = ['Menos de 1 ano', '1 a 3 anos', '4 a 6 anos', '7 a 10 anos', 'Mais de 10 anos']
    exp_counts = [sum(1 for d in data if d['B'] == c) for c in exp_cats]
    
    panel1_x, panel1_y = 60, 160
    p1_w, p1_h = 650, 480
    
    # Background card
    ctx.set_source_rgb(0.97, 0.98, 0.99)
    round_rect(ctx, panel1_x, panel1_y, p1_w, p1_h, 8)
    ctx.fill()
    ctx.set_source_rgb(0.85, 0.88, 0.92)
    ctx.set_line_width(1.5)
    round_rect(ctx, panel1_x, panel1_y, p1_w, p1_h, 8)
    ctx.stroke()
    
    bar_colors = [
        (0.2, 0.5, 0.8),
        (0.15, 0.4, 0.75),
        (0.1, 0.6, 0.5),
        (0.85, 0.45, 0.1),
        (0.7, 0.2, 0.3)
    ]
    
    max_val = 10
    for i, (cat, count) in enumerate(zip(exp_cats, exp_counts)):
        by = panel1_y + 40 + i * 85
        pct = (count / total_n) * 100
        draw_text(ctx, cat, panel1_x + 25, by + 18, size=15, bold=True, color=(0.2, 0.25, 0.3))
        
        # Bar background
        bar_x = panel1_x + 180
        bar_max_w = 340
        ctx.set_source_rgb(0.9, 0.92, 0.95)
        round_rect(ctx, bar_x, by, bar_max_w, 26, 5)
        ctx.fill()
        
        # Filled bar
        fill_w = (count / max_val) * bar_max_w
        ctx.set_source_rgb(*bar_colors[i])
        round_rect(ctx, bar_x, by, fill_w, 26, 5)
        ctx.fill()
        
        # Label
        lbl = f"{count} ({pct:.1f}%)"
        draw_text(ctx, lbl, bar_x + fill_w + 12, by + 19, size=15, bold=True, color=(0.1, 0.2, 0.35))
        
    # Panel 2: Participação em Grandes Projetos (Donut / Card chart)
    draw_text(ctx, "B. Atuação em Projetos de Grande Escala", 760, 130, size=18, bold=True, color=(0.15, 0.25, 0.45))
    panel2_x, panel2_y = 760, 160
    p2_w, p2_h = 580, 480
    
    ctx.set_source_rgb(0.97, 0.98, 0.99)
    round_rect(ctx, panel2_x, panel2_y, p2_w, p2_h, 8)
    ctx.fill()
    ctx.set_source_rgb(0.85, 0.88, 0.92)
    ctx.set_line_width(1.5)
    round_rect(ctx, panel2_x, panel2_y, p2_w, p2_h, 8)
    ctx.stroke()
    
    sim_count = sum(1 for d in data if d['E'] == 'Sim')
    nao_count = sum(1 for d in data if d['E'] == 'Não')
    
    # Donut center
    cx, cy = panel2_x + 190, panel2_y + 230
    radius = 120
    inner_r = 70
    
    # Slice 1: Sim (52.2%)
    angle_sim = (sim_count / total_n) * 2 * math.pi
    ctx.set_source_rgb(0.12, 0.45, 0.75)
    ctx.arc(cx, cy, radius, -math.pi/2, -math.pi/2 + angle_sim)
    ctx.arc_negative(cx, cy, inner_r, -math.pi/2 + angle_sim, -math.pi/2)
    ctx.close_path()
    ctx.fill()
    
    # Slice 2: Nao (47.8%)
    ctx.set_source_rgb(0.85, 0.45, 0.15)
    ctx.arc(cx, cy, radius, -math.pi/2 + angle_sim, 3*math.pi/2)
    ctx.arc_negative(cx, cy, inner_r, 3*math.pi/2, -math.pi/2 + angle_sim)
    ctx.close_path()
    ctx.fill()
    
    # Center text
    draw_text(ctx, f"{total_n}", cx, cy + 8, size=32, bold=True, color=(0.1, 0.2, 0.35), align='center')
    draw_text(ctx, "Total", cx, cy + 28, size=13, bold=False, color=(0.45, 0.5, 0.55), align='center')
    
    # Legend
    # Sim
    ctx.set_source_rgb(0.12, 0.45, 0.75)
    round_rect(ctx, panel2_x + 360, panel2_y + 160, 22, 22, 4)
    ctx.fill()
    draw_text(ctx, f"Sim ({sim_count})", panel2_x + 395, panel2_y + 178, size=17, bold=True, color=(0.1, 0.2, 0.35))
    draw_text(ctx, f"{sim_count/total_n*100:.1f}% da amostra", panel2_x + 395, panel2_y + 198, size=13, color=(0.45, 0.5, 0.55))
    
    # Nao
    ctx.set_source_rgb(0.85, 0.45, 0.15)
    round_rect(ctx, panel2_x + 360, panel2_y + 240, 22, 22, 4)
    ctx.fill()
    draw_text(ctx, f"Não ({nao_count})", panel2_x + 395, panel2_y + 258, size=17, bold=True, color=(0.1, 0.2, 0.35))
    draw_text(ctx, f"{nao_count/total_n*100:.1f}% da amostra", panel2_x + 395, panel2_y + 278, size=13, color=(0.45, 0.5, 0.55))
    
    # Note on large project definition
    draw_text(ctx, "* Critério: Equipes com > 5 desenvolvedores e/ou projetos com > 6 meses.", panel2_x + 30, panel2_y + 430, size=13, color=(0.45, 0.5, 0.55))
    
    # Footer source
    draw_text(ctx, "Fonte: Dados da pesquisa aplicada pelo autor (2025).", 50, 715, size=14, color=(0.45, 0.5, 0.55))
    
    surface.write_to_png("04-figuras/fig_demografia_experiencia.png")
    print("Saved 04-figuras/fig_demografia_experiencia.png")

# -------------------------------------------------------------
# FIGURA 2: Nível de Proficiência Técnica (JS vs TS)
# -------------------------------------------------------------
def generate_fig2():
    w, h = 1300, 700
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    draw_text(ctx, "Distribuição da Proficiência Técnica Declarada: JavaScript vs TypeScript", 50, 50, size=24, bold=True, color=(0.08, 0.18, 0.36))
    draw_text(ctx, "Comparativo percentual de nível de domínio declarado pelos desenvolvedores (N = 23)", 50, 80, size=15, color=(0.4, 0.45, 0.5))

    levels = ['Nunca utilizei', 'Iniciante', 'Intermediário', 'Avançado', 'Especialista']
    js_counts = [sum(1 for d in data if d['C'] == l) for l in levels]
    ts_counts = [sum(1 for d in data if d['D'] == l) for l in levels]
    
    ox, oy = 150, 160
    plot_w, plot_h = 1050, 420
    
    # Gridlines
    ctx.set_line_width(1)
    for p in range(0, 60, 10):
        y_pos = oy + plot_h - (p / 50.0) * plot_h
        ctx.set_source_rgb(0.9, 0.92, 0.95)
        ctx.move_to(ox - 10, y_pos)
        ctx.line_to(ox + plot_w, y_pos)
        ctx.stroke()
        draw_text(ctx, f"{p}%", ox - 20, y_pos + 5, size=13, color=(0.45, 0.5, 0.55), align='right')
        
    group_spacing = plot_w / len(levels)
    bar_w = 48
    
    for i, lvl in enumerate(levels):
        gx = ox + i * group_spacing + group_spacing / 2
        
        # JS bar (Gold/Amber)
        js_pct = (js_counts[i] / total_n) * 100
        js_h = (js_pct / 50.0) * plot_h
        bx_js = gx - bar_w - 4
        by_js = oy + plot_h - js_h
        ctx.set_source_rgb(0.9, 0.65, 0.1)
        round_rect(ctx, bx_js, by_js, bar_w, js_h, 4)
        ctx.fill()
        if js_counts[i] > 0:
            draw_text(ctx, f"{js_pct:.1f}%", bx_js + bar_w/2, by_js - 8, size=13, bold=True, color=(0.7, 0.45, 0.05), align='center')
            draw_text(ctx, f"({js_counts[i]})", bx_js + bar_w/2, by_js + 18, size=11, bold=True, color=(1, 1, 1), align='center')

        # TS bar (Blue)
        ts_pct = (ts_counts[i] / total_n) * 100
        ts_h = (ts_pct / 50.0) * plot_h
        bx_ts = gx + 4
        by_ts = oy + plot_h - ts_h
        ctx.set_source_rgb(0.15, 0.42, 0.8)
        round_rect(ctx, bx_ts, by_ts, bar_w, ts_h, 4)
        ctx.fill()
        if ts_counts[i] > 0:
            draw_text(ctx, f"{ts_pct:.1f}%", bx_ts + bar_w/2, by_ts - 8, size=13, bold=True, color=(0.1, 0.3, 0.65), align='center')
            draw_text(ctx, f"({ts_counts[i]})", bx_ts + bar_w/2, by_ts + 18, size=11, bold=True, color=(1, 1, 1), align='center')
            
        # X Category Label
        draw_text(ctx, lvl, gx, oy + plot_h + 30, size=15, bold=True, color=(0.15, 0.25, 0.35), align='center')
        
    # Baseline
    ctx.set_source_rgb(0.3, 0.35, 0.4)
    ctx.set_line_width(2)
    ctx.move_to(ox - 10, oy + plot_h)
    ctx.line_to(ox + plot_w, oy + plot_h)
    ctx.stroke()
    
    # Legend
    leg_x = 900
    ctx.set_source_rgb(0.9, 0.65, 0.1)
    round_rect(ctx, leg_x, 85, 20, 20, 3)
    ctx.fill()
    draw_text(ctx, "JavaScript", leg_x + 30, 101, size=15, bold=True, color=(0.2, 0.2, 0.2))

    ctx.set_source_rgb(0.15, 0.42, 0.8)
    round_rect(ctx, leg_x + 160, 85, 20, 20, 3)
    ctx.fill()
    draw_text(ctx, "TypeScript", leg_x + 190, 101, size=15, bold=True, color=(0.2, 0.2, 0.2))
    
    draw_text(ctx, "Fonte: Dados da pesquisa aplicada pelo autor (2025).", 50, 665, size=14, color=(0.45, 0.5, 0.55))
    surface.write_to_png("04-figuras/fig_nivel_proficiencia.png")
    print("Saved 04-figuras/fig_nivel_proficiencia.png")

# -------------------------------------------------------------
# HELPER FOR LIKERT COMPARATIVE BARS (Blocos A, B, C, D)
# -------------------------------------------------------------
def generate_likert_block_chart(filename, title, subtitle, items_keys_labels):
    w, h = 1500, 150 + len(items_keys_labels) * 100
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    draw_text(ctx, title, 50, 48, size=24, bold=True, color=(0.08, 0.18, 0.36))
    draw_text(ctx, subtitle, 50, 78, size=15, color=(0.4, 0.45, 0.5))
    
    # Legend nicely formatted inside right area
    leg_x = 830
    # Iniciantes (<3 anos)
    ctx.set_source_rgb(0.25, 0.6, 0.85)
    round_rect(ctx, leg_x, 58, 18, 18, 3)
    ctx.fill()
    draw_text(ctx, f"Iniciantes (<3 anos, N={len(g_inic)})", leg_x + 26, 73, size=14, bold=True, color=(0.2, 0.2, 0.2))
    
    # Experientes (>=4 anos)
    ctx.set_source_rgb(0.12, 0.25, 0.55)
    round_rect(ctx, leg_x + 300, 58, 18, 18, 3)
    ctx.fill()
    draw_text(ctx, f"Experientes (>=4 anos, N={len(g_exp)})", leg_x + 326, 73, size=14, bold=True, color=(0.2, 0.2, 0.2))

    start_y = 135
    bar_area_x = 840
    bar_max_w = 520
    
    for idx, (col_key, label_text) in enumerate(items_keys_labels):
        row_y = start_y + idx * 100
        
        # Subtle separator / background card
        ctx.set_source_rgb(0.97, 0.98, 0.99) if idx % 2 == 0 else ctx.set_source_rgb(1, 1, 1)
        round_rect(ctx, 40, row_y - 12, w - 80, 92, 6)
        ctx.fill()
        
        # Question label (wrap if needed)
        lines = []
        words = label_text.split()
        cur_line = []
        for word in words:
            if len(' '.join(cur_line + [word])) > 66:
                lines.append(' '.join(cur_line))
                cur_line = [word]
            else:
                cur_line.append(word)
        if cur_line:
            lines.append(' '.join(cur_line))
            
        for l_i, l_text in enumerate(lines):
            draw_text(ctx, l_text, 55, row_y + 14 + l_i * 22, size=14, bold=(l_i==0), color=(0.12, 0.2, 0.3))
            
        v_inic = [float(d[col_key]) for d in g_inic if d.get(col_key) is not None]
        v_exp = [float(d[col_key]) for d in g_exp if d.get(col_key) is not None]
        m_i = statistics.mean(v_inic)
        m_e = statistics.mean(v_exp)
        
        # Scale grid lines for 1..5
        for s in range(1, 6):
            gx = bar_area_x + ((s - 1) / 4.0) * bar_max_w
            ctx.set_source_rgb(0.88, 0.9, 0.93)
            ctx.set_line_width(1)
            ctx.move_to(gx, row_y - 6)
            ctx.line_to(gx, row_y + 72)
            ctx.stroke()
            if idx == 0:
                draw_text(ctx, str(s), gx, row_y - 14, size=12, color=(0.5, 0.55, 0.6), align='center')
                
        # Draw Bar 1: Iniciantes (Light Blue)
        b1_y = row_y + 6
        b1_w = ((m_i - 1) / 4.0) * bar_max_w
        ctx.set_source_rgb(0.9, 0.92, 0.96)
        round_rect(ctx, bar_area_x, b1_y, bar_max_w, 24, 4)
        ctx.fill()
        ctx.set_source_rgb(0.25, 0.6, 0.85)
        round_rect(ctx, bar_area_x, b1_y, b1_w, 24, 4)
        ctx.fill()
        draw_text(ctx, f"{m_i:.2f}", bar_area_x + b1_w + 10, b1_y + 17, size=13, bold=True, color=(0.18, 0.45, 0.7))
        
        # Draw Bar 2: Experientes (Navy Blue)
        b2_y = row_y + 38
        b2_w = ((m_e - 1) / 4.0) * bar_max_w
        ctx.set_source_rgb(0.9, 0.92, 0.96)
        round_rect(ctx, bar_area_x, b2_y, bar_max_w, 24, 4)
        ctx.fill()
        ctx.set_source_rgb(0.12, 0.25, 0.55)
        round_rect(ctx, bar_area_x, b2_y, b2_w, 24, 4)
        ctx.fill()
        draw_text(ctx, f"{m_e:.2f}", bar_area_x + b2_w + 10, b2_y + 17, size=13, bold=True, color=(0.08, 0.18, 0.4))

    draw_text(ctx, "Fonte: Dados da pesquisa aplicada pelo autor (2025). Escala Likert de 1 (Discordo totalmente) a 5 (Concordo totalmente).", 50, h - 25, size=13, color=(0.45, 0.5, 0.55))
    surface.write_to_png(filename)
    print(f"Saved {filename}")

# -------------------------------------------------------------
# FIGURA 3: Bloco A - Produtividade e Desenvolvimento
# -------------------------------------------------------------
def generate_fig3():
    items = [
        ('F', 'Desenvolve funcionalidades mais rápido em JavaScript do que em TypeScript'),
        ('G', 'O TypeScript aumenta a sua produtividade geral no desenvolvimento'),
        ('H', 'A curva de aprendizado do TypeScript é mais íngreme que a do JavaScript'),
        ('I', 'JavaScript é mais fácil de entender e ensinar a novos desenvolvedores'),
        ('J', 'TypeScript ajuda a detectar erros mais cedo durante o desenvolvimento'),
        ('K', 'JavaScript permite prototipar aplicações com muito mais rapidez')
    ]
    generate_likert_block_chart(
        "04-figuras/fig_blocoA_produtividade.png",
        "Bloco A: Produtividade e Desenvolvimento Ágil",
        "Comparativo de médias na escala Likert (1 a 5) entre Iniciantes (<3 anos) e Experientes (>=4 anos)",
        items
    )

# -------------------------------------------------------------
# FIGURA 4: Bloco B - Qualidade e Manutenção do Código
# -------------------------------------------------------------
def generate_fig4():
    items = [
        ('L', 'Código em TypeScript é mais legível do que código em JavaScript'),
        ('M', 'Projetos em TypeScript tendem a ser mais fáceis de manter a longo prazo'),
        ('N', 'JavaScript tende a gerar mais bugs devido à ausência de tipagem estática'),
        ('O', 'TypeScript torna o código excessivamente verboso e difícil de ler'),
        ('P', 'TypeScript melhora a padronização e governança em equipes grandes'),
        ('Q', 'JavaScript é mais flexível e viabiliza soluções rápidas para problemas simples')
    ]
    generate_likert_block_chart(
        "04-figuras/fig_blocoB_qualidade_manutencao.png",
        "Bloco B: Qualidade de Código, Manutenibilidade e Confiabilidade",
        "Comparativo de médias na escala Likert (1 a 5) entre Iniciantes (<3 anos) e Experientes (>=4 anos)",
        items
    )

# -------------------------------------------------------------
# FIGURA 5: Bloco C - Compatibilidade e Ferramentas
# -------------------------------------------------------------
def generate_fig5():
    items = [
        ('R', 'TypeScript possui excelente compatibilidade com frameworks (React, Vue, Angular)'),
        ('S', 'É fácil integrar/migrar TypeScript em projetos originalmente em JavaScript'),
        ('T', 'Ferramentas de desenvolvimento (VS Code, ESLint) suportam melhor o TypeScript'),
        ('U', 'JavaScript ainda é mais amplamente suportado e compatível com projetos legados')
    ]
    generate_likert_block_chart(
        "04-figuras/fig_blocoC_compatibilidade_ferramentas.png",
        "Bloco C: Compatibilidade, Ecossistema e Ferramentas",
        "Comparativo de médias na escala Likert (1 a 5) entre Iniciantes (<3 anos) e Experientes (>=4 anos)",
        items
    )

# -------------------------------------------------------------
# FIGURA 6: Bloco D - Preferências e Perspectivas Pessoais
# -------------------------------------------------------------
def generate_fig6():
    items = [
        ('V', 'Prefiro trabalhar com TypeScript na criação de novos projetos'),
        ('W', 'Sinto-me mais seguro e confiante ao escrever código em TypeScript'),
        ('X', 'Acredito que o TypeScript será o padrão mais relevante para o futuro do front-end'),
        ('Y', 'Prefiro utilizar JavaScript pela simplicidade, agilidade e flexibilidade'),
        ('Z', 'Em equipes grandes, o TypeScript traz expressivamente mais benefícios que o JavaScript')
    ]
    generate_likert_block_chart(
        "04-figuras/fig_blocoD_preferencias_futuro.png",
        "Bloco D: Preferências Pessoais, Confiança e Visão de Futuro",
        "Comparativo de médias na escala Likert (1 a 5) entre Iniciantes (<3 anos) e Experientes (>=4 anos)",
        items
    )

# -------------------------------------------------------------
# FIGURA 7: Gráfico de Divergência Cognitiva (Delta Experientes - Iniciantes)
# -------------------------------------------------------------
def generate_fig7():
    w, h = 1450, 780
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    draw_text(ctx, "Divergência Perceptual: Experientes vs Iniciantes (Δ = Média_Exp - Média_Inic)", 50, 50, size=24, bold=True, color=(0.08, 0.18, 0.36))
    draw_text(ctx, "Itens com maiores contrastes de opinião entre desenvolvedores seniores e juniores", 50, 80, size=15, color=(0.4, 0.45, 0.5))

    diff_items = [
        ("TS aumenta produtividade geral", +1.29, "Favorável ao TS com experiência"),
        ("Prototipagem rápida em JS", -1.17, "Iniciantes valorizam mais agilidade JS"),
        ("Preferência por TS em novos projetos", +1.13, "Experientes priorizam TS em greenfield"),
        ("Preferência por JS (simplicidade)", -1.07, "Iniciantes apegam-se à flexibilidade JS"),
        ("Confiança ao codificar em TS", +1.05, "Seniores sentem maior segurança técnica"),
        ("Facilidade de manutenção a longo prazo", +1.02, "Seniores valorizam manutenibilidade"),
        ("Detecção precoce de erros em TS", +0.99, "Seniores dependem do compilador"),
        ("Suporte superior de IDE / Tooling", +0.84, "IntelliSense aproveitado por seniores"),
        ("Dificuldade na migração JS -> TS", -0.63, "Seniores reconhecem atritos reais na migração"),
        ("TS torna código verboso / difícil", -0.46, "Iniciantes sentem maior sobrecarga sintática")
    ]
    
    cx = 720
    start_y = 140
    row_h = 56
    max_scale = 1.6 # max delta
    bar_half_w = 460
    
    # Zero vertical line
    ctx.set_source_rgb(0.7, 0.75, 0.8)
    ctx.set_line_width(2)
    ctx.move_to(cx, start_y - 20)
    ctx.line_to(cx, start_y + len(diff_items) * row_h + 10)
    ctx.stroke()
    
    draw_text(ctx, "← Maior Concordância Iniciantes", cx - 40, start_y - 25, size=13, bold=True, color=(0.75, 0.35, 0.1), align='right')
    draw_text(ctx, "Maior Concordância Experientes →", cx + 40, start_y - 25, size=13, bold=True, color=(0.1, 0.35, 0.7), align='left')

    for idx, (label, delta, note) in enumerate(diff_items):
        ry = start_y + idx * row_h
        
        # Grid line
        ctx.set_source_rgb(0.93, 0.94, 0.96)
        ctx.set_line_width(1)
        ctx.move_to(80, ry + 20)
        ctx.line_to(w - 80, ry + 20)
        ctx.stroke()
        
        # Label on left
        draw_text(ctx, label, 70, ry + 16, size=14, bold=True, color=(0.15, 0.2, 0.3))
        
        # Bar
        bar_len = (abs(delta) / max_scale) * bar_half_w
        if delta >= 0:
            bx = cx
            ctx.set_source_rgb(0.12, 0.4, 0.75)
            round_rect(ctx, bx, ry, bar_len, 24, 4)
            ctx.fill()
            draw_text(ctx, f"+{delta:.2f}", cx + bar_len + 10, ry + 17, size=13, bold=True, color=(0.08, 0.3, 0.65))
        else:
            bx = cx - bar_len
            ctx.set_source_rgb(0.85, 0.4, 0.15)
            round_rect(ctx, bx, ry, bar_len, 24, 4)
            ctx.fill()
            draw_text(ctx, f"{delta:.2f}", bx - 10, ry + 17, size=13, bold=True, color=(0.75, 0.3, 0.05), align='right')

    draw_text(ctx, "Fonte: Dados da pesquisa aplicada pelo autor (2025). Valores representam a diferença absoluta de médias entre os grupos.", 50, h - 25, size=13, color=(0.45, 0.5, 0.55))
    surface.write_to_png("04-figuras/fig_comparativo_iniciantes_experientes.png")
    print("Saved 04-figuras/fig_comparativo_iniciantes_experientes.png")

generate_fig1()
generate_fig2()
generate_fig3()
generate_fig4()
generate_fig5()
generate_fig6()
generate_fig7()
print("All 7 figures generated successfully!")
