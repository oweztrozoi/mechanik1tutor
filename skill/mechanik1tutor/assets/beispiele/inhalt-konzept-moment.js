/* Konzept: Moment einer Kraft */
const CONFIG = {
  title: "Moment einer Kraft bezüglich eines Punktes",
  subtitle: "Warum dreht eine Kraft – und wie stark? $\\;\\vec M_Q=\\vec r\\times\\vec F$",
  tags: ["Konzept"],
  autoplayMs: 4800
};
const LEGEND = [
  {c:"B", label:"Kraft F"}, {c:"A", label:"Ortsvektor r (Q → Wirkungslinie)"}, {c:"C", label:"Normalabstand a"},
  {c:"F", label:"Komponenten F_x, F_y"}, {c:"E", label:"Moment M_Q"}
];
// 50 px pro Meter, Q im Ursprung bei (150, 300); y nach oben
const P = (x,y) => [150 + 50*x, 300 - 50*y];
function build(){
  viewbox(600,400);
  const Q=P(0,0), A=P(3,2), foot=P(0.96,-0.72), g1=P(0.3,-1.6), g2=P(4.5,4);
  at(0); poly([[105,335],[125,175],[265,140],[350,185],[340,330],[215,370]],{close:true,c:"var(--struct)",fill:"var(--struct)",fillOpacity:0.08,id:"body"});
  at(0); point(...Q,"Q",{dx:-14,dy:14});
  at(0); point(...A,"A",{dx:14,dy:10});
  at(0,4); force(...A,53.13,100,"B","F",{mode:"tail",id:"F",loff:-16});
  at(1); line(...g1,...g2,{c:"B",dash:true,id:"g"}); label(g2[0]+10,g2[1]+8,"g","B");
  at(1,1); force(...P(1.44,-0.08),53.13,100,"B","F",{mode:"tail",loff:-16});
  at(2); arrow(...Q,...A,"A","r",{id:"r",loff:16});
  at(0); axes(40,370,{dirs:{x:"right",y:"up"},len:30});
  at(3); line(...Q,...foot,{c:"C",w:3,id:"a"}); label((Q[0]+foot[0])/2-14,(Q[1]+foot[1])/2+8,"a","C");
  at(3); poly([[foot[0]-6.4,foot[1]-4.8],[foot[0]-1.6,foot[1]-11.2],[foot[0]+4.8,foot[1]-6.4]],{c:"C",w:1.5});
  at(3); moment(...Q,30,true,"E","M_Q",{start:300,span:230,loff:18,id:"M"});
  at(4,4); force(...A,0,60,"F","F_x",{mode:"tail",id:"Fx",loff:14});
  at(4,4); force(...A,90,80,"F","F_y",{mode:"tail",id:"Fy",loff:-16});
  at(4,4); dim(...Q,...P(3,0),"x_A = 3 m",{off:44}); dim(...P(3,0),...A,"y_A = 2 m",{off:44});
  at(5); force(...Q,53.13,100,"B","F",{mode:"tail",id:"FQ",loff:-16});
}
const STEPS = [
  { title:"Was soll berechnet werden?",
    text:"Auf einen starren Körper wirkt im Punkt $A$ die Kraft $\\cB{F}=10\\,$kN. Frage: Wie stark versucht sie, den Körper um den Punkt $Q$ zu <b>drehen</b>? Genau das misst das Moment $\\cE{M_Q}$.",
    hl:["F"] },
  { title:"Nur die Wirkungslinie zählt",
    text:"Am <b>starren</b> Körper darf eine Kraft entlang ihrer Wirkungslinie $\\cB{g}$ verschoben werden. Die Drehwirkung bleibt gleich – deshalb darf $\\vec r$ zu <b>irgendeinem</b> Punkt von $\\cB{g}$ zeigen.",
    hl:["g"] },
  { title:"Definition als Kreuzprodukt",
    text:"$\\cA{\\vec r}$ zeigt von $Q$ zu einem Punkt der Wirkungslinie (hier $A$). Das Moment ist ein <b>gebundener Vektor</b>, normal zur Zeichenebene, Richtung nach der Rechte-Hand-Regel.",
    tex:"\\cE{\\vec M_Q}=\\cA{\\vec r}\\times\\cB{\\vec F}",
    hl:["r","F"] },
  { title:"Anschaulich: Kraft × Normalabstand",
    text:"Der Betrag ist Kraft mal <b>Normalabstand</b> $\\cC{a}$ von $Q$ zur Wirkungslinie. Je weiter weg die Wirkungslinie, desto größer die Drehwirkung. Hier dreht $\\cB{F}$ gegen den Uhrzeigersinn → positiv um $z$.",
    tex:"\\cE{M_Q}=\\cC{a}\\cdot\\cB{F}=\\cC{1{,}2\\,\\text{m}}\\cdot\\cB{10\\,\\text{kN}}=\\cE{12\\,\\text{kNm}}",
    hl:["a","M"] },
  { title:"Rechnen mit Komponenten",
    ask:"Zerlege $\\cB{F}$ in $\\cF{F_x}=6\\,$kN und $\\cF{F_y}=8\\,$kN. Welches Moment liefert jede Komponente um $Q$? Achte auf den Drehsinn!",
    text:"$\\cF{F_y}$ hat den Hebelarm $x_A$ und dreht gegen den Uhrzeigersinn (+); $\\cF{F_x}$ hat den Hebelarm $y_A$ und dreht im Uhrzeigersinn (−). Damit:",
    tex:"\\cE{M_Q}=x_A\\cF{F_y}-y_A\\cF{F_x}=3\\cdot\\cF{8}-2\\cdot\\cF{6}=\\cE{12\\,\\text{kNm}}\\;\\checkmark",
    hl:["Fx","Fy"] },
  { title:"Reduktion in den Punkt Q",
    text:"Bringt man in $Q$ die Kräfte $\\cB{\\vec F}$ und $-\\cB{\\vec F}$ an (ändert nichts), bildet $-\\cB{\\vec F}$ mit der Originalkraft ein Kräftepaar. Ergebnis: <b>$\\cB{\\vec F}$ in $Q$ plus $\\cE{\\vec M_Q}$</b> wirkt auf den starren Körper genauso wie die ursprüngliche Kraft.",
    tex:"\\cB{\\vec F}\\text{ auf }g\\;\\equiv\\;\\cB{\\vec F}\\text{ in }Q\\;+\\;\\cE{\\vec M_Q}=\\cA{\\vec r}\\times\\cB{\\vec F}",
    hl:["FQ","M"] }
];
const PRAXIS = {
  title: "Radmutter mit dem Radkreuz lösen",
  text: "Am Radkreuz ist $Q$ die Mutter. Drückst du senkrecht zum Griff, ist der Normalabstand $\\cC{a}$ gleich der Grifflänge – maximales Moment. Ziehst du schräg, wird $\\cC{a}$ kleiner und es dreht schwerer, obwohl $\\cB{F}$ gleich bleibt. Deshalb steckt man bei festsitzenden Muttern ein Rohr auf den Griff: größeres $\\cC{a}$ → größeres $\\cE{M_Q}=\\cC{a}\\cB{F}$."
};
