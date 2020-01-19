************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_telescopic
* View Name:     schematic
* Netlisted on:  Sep 11 21:39:36 2019
************************************************************************

*.BIPOLAR
*.RESI = 2000 
*.RESVAL
*.CAPVAL
*.DIOPERI
*.DIOAREA
*.EQUATION
*.SCALE METER
*.MEGA
.PARAM

*.GLOBAL vdd!
+        gnd!

*.PIN vdd!
*+    gnd!

************************************************************************
* Library Name: OTA_class
* Cell Name:    single_ended_telescopic
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_telescopic Vbiasn Vbiasp2 Vinn Vinp Voutp
*.PININFO Vbiasn:I Vbiasp2:I Vinn:I Vinp:I Voutp:O
MM3 Voutp Vinp net11 gnd! nmos_rvt w=WA l=LA nfin=nA
MM0 net13 Vinn net11 gnd! nmos_rvt w=WA l=LA nfin=nA
MM4 net11 Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM6 net13 Vbiasp2 net016 vdd! pmos_rvt w=WA l=LA nfin=nA
MM5 Voutp Vbiasp2 net014 vdd! pmos_rvt w=WA l=LA nfin=nA
MM1 net014 net13 vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM2 net016 net13 vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasp Biasn Vbiasp1 Vbiasp2
*.PININFO Biasn:I Vbiasp1:O Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM1 Vbiasp2 Vbiasp2 Vbiasp1 vdd! pmos_rvt w=WA l=LA nfin=nA
MM3 Vbiasp1 Vbiasp1 vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR13_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM0 Vbiasn Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM1 Vbiasn Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasp2 Vinn Vinp Voutp single_ended_telescopic
xiLG_load_biasp Biasn LG_Vbiasp1 LG_Vbiasp2 LG_load_biasp
xibCR13_2 Biasn Vbiasp CR13_2
.END