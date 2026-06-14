from IPython.display import HTML, display
from math import sin, cos, sqrt

def buildQubitHTML(phase):
    centreX = 80
    centreY = 80
    radius = 50
    px = centreX + radius * cos(phase)
    py = centreY - radius * sin(phase)

    zero_component = round(cos(phase), 3)
    if zero_component == -0.0: zero_component = 0.0
    one_component = round(sin(phase), 3)
    if one_component == -0.0: one_component = 0.0
    one_component_symbol = "&#x2212;" if one_component < 0 else "+"
    one_component_abs = abs(one_component)

    return f'''
    <svg width="160" height="160">
        <circle cx="{centreX}" cy="{centreY}" r="{radius}" stroke="black" stroke-width="1" fill="white"/>
        <text x="{centreX}" y="{centreY - radius - 15}" dominant-baseline="middle" text-anchor="middle">|1&#x27E9;</text>
        <text x="{centreX}" y="{centreY + radius + 15}" dominant-baseline="middle" text-anchor="middle">-|1&#x27E9;</text>
        <text x="{centreX + radius + 15}" y="{centreY}" dominant-baseline="middle" text-anchor="middle">|0&#x27E9;</text>
        <text x="{centreX - radius - 15}" y="{centreY}" dominant-baseline="middle" text-anchor="middle">-|0&#x27E9;</text>
        <text x="{centreX + (1/sqrt(2) * (radius + 15))}" y="{centreY - (1/sqrt(2) * (radius + 15))}" dominant-baseline="middle" text-anchor="middle">|+&#x27E9;</text>
        <text x="{centreX - (1/sqrt(2) * (radius + 15))}" y="{centreY + (1/sqrt(2) * (radius + 15))}" dominant-baseline="middle" text-anchor="middle">-|+&#x27E9;</text>
        <text x="{centreX + (1/sqrt(2) * (radius + 15))}" y="{centreY + (1/sqrt(2) * (radius + 15))}" dominant-baseline="middle" text-anchor="middle">|-&#x27E9;</text>
        <text x="{centreX - (1/sqrt(2) * (radius + 15))}" y="{centreY - (1/sqrt(2) * (radius + 15))}" dominant-baseline="middle" text-anchor="middle">-|-&#x27E9;</text>
        <circle cx="{px}" cy="{py}" r="5" stroke="black" stroke-width="1" fill="black"/>
        <line x1="{centreX}" y1="{centreY}" x2="{px}" y2="{py}" stroke="black"/>
        <line stroke-dasharray="2, 1" x1="{centreX}" y1="{centreY}" x2="{px}" y2="{centreY}" stroke="blue"/>
        <line stroke-dasharray="2, 1" x1="{px}" y1="{centreY}" x2="{px}" y2="{py}" stroke="blue"/>
    </svg>
    <div style="display:flex; align-items:center; gap:10px; font-family:serif; font-size:16px; margin-top:4px;">
        <span style="border-left:2px solid black; border-right:2px solid black; padding:2px 10px; line-height:2.4; text-align:right;">
            {zero_component:.3f}<br>{one_component:.3f}
        </span>
        <span>=</span>
        <span>{zero_component:.3f}&thinsp;|0&#x27E9; {one_component_symbol} {one_component_abs:.3f}&thinsp;|1&#x27E9;</span>
    </div>'''

def drawQubit(phase):
    display(HTML(buildQubitHTML(phase)))
