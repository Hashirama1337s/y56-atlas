from PIL import Image, ImageDraw, ImageFont
D=''
fr=[Image.open(D+f'frames/f{i:02d}.png').convert('RGB') for i in range(48)]
q=[im.resize((600,600),Image.LANCZOS) for im in fr]
q[0].save(D+'y56_to_fermat.gif',save_all=True,append_images=q[1:],duration=[900]+[110]*47,loop=0,optimize=True)
idx=[0,7,14,33,47]
cap=["Y56: 56 real lines, |kappa| 6.364","between: 40 lines, 5.18","wall: 8 nodes, 24 lines, 4","between: 8 lines, 2.00","Fermat-type: 8 lines, 0"]
W=520; H=int(W*750/900)
S=Image.new('RGB',(W*5,H+80),"#0b0d12"); dr=ImageDraw.Draw(S)
try: f=ImageFont.truetype("arial.ttf",19)
except Exception: f=ImageFont.load_default()
for j,(i,c) in enumerate(zip(idx,cap)):
    im=fr[i].crop((0,110,900,860)).resize((W,H),Image.LANCZOS); S.paste(im,(j*W,36))
    dr.text((j*W+8,6),c,fill="#e6f1ff",font=f)
dr.text((8,H+48),"EXPLORATORY  |  line counts numerical  |  same camera, family F(1,b,-1), b = sqrt|kappa|",fill="#9fb4c8",font=f)
S.save(D+'y56_family_strip.png')
