** Switch subckts

.subckt Switch_NMOS  D G S
M0 D G S S NMOS
.ends Switch_NMOS

.subckt Switch_PMOS  D G S
M0 D G S S PMOS
.ends Switch_PMOS

* SCM subckts

.subckt SCM_NMOS DA DB S
M0 DA DA S S NMOS
M1 DB DA S S NMOS
.ends SCM_NMOS

.subckt SCM_PMOS DA DB S
M0 DA DA S S PMOS
M1 DB DA S S PMOS
.ends SCM_PMOS

.subckt SCM_NMOS_B DA DB S B
M0 DA DA S B NMOS
M1 DB DA S B NMOS
.ends SCM_NMOS_B

.subckt SCM_PMOS_B DA DB S B
M0 DA DA S B PMOS
M1 DB DA S B PMOS
.ends SCM_PMOS_B

* CMFB subckts

.subckt CMFB_NMOS DA DB GB S
M0 DA DA S S NMOS
M1 DB GB S S NMOS
.ends CMFB_NMOS

.subckt CMFB_PMOS DA DB GB S
M0 DA DA S S PMOS
M1 DB GB S S PMOS
.ends CMFB_PMOS

.subckt CMFB_NMOS_B DA DB GB S B
M0 DA DA S B NMOS
M1 DB GB S B NMOS
.ends CMFB_NMOS_B

.subckt CMFB_PMOS_B DA DB GB S B
M0 DA DA S B PMOS
M1 DB GB S B PMOS
.ends CMFB_PMOS_B

* CMC subckts
.subckt CMC_PMOS DA DB SA SB G
M0 DA G SA SA PMOS
M1 DB G SB SB PMOS
.ends CMC_PMOS

.subckt CMC_NMOS DA DB SA SB G
M0 DA G SA SA NMOS
M1 DB G SB SB NMOS
.ends CMC_NMOS

.subckt CMC_PMOS_B DA DB SA SB G B
M0 DA G SA B PMOS
M1 DB G SB B PMOS
.ends CMC_PMOS

.subckt CMC_NMOS_B DA DB SA SB G B
M0 DA G SA B NMOS
M1 DB G SB B NMOS
.ends CMC_NMOS

* CMC_*_S subckts
.subckt CMC_NMOS_S  DA DB G S
M0 DA G S S NMOS
M1 DB G S S NMOS
.ends CMC_NMOS_S

.subckt CMC_PMOS_S  DA DB G S
M0 DA G S S PMOS
M1 DB G S S PMOS
.ends CMC_PMOS_S

.subckt CMC_NMOS_SB  DA DB G S B
M0 DA G S B NMOS
M1 DB G S B NMOS
.ends CMC_NMOS_SB

.subckt CMC_PMOS_SB  DA DB G S B
M0 DA G S B PMOS
M1 DB G S B PMOS
.ends CMC_PMOS_SB

* CASCODED_CMC subckts
.subckt CASCODED_CMC_PMOS DA GA DB S
M0 DA GA SA SA PMOS
M1 DB GA SB SB PMOS
M2 SA DB S S PMOS
M3 SB DB S S PMOS
.ends CASCODED_CMC_PMOS

.subckt CASCODED_CMC_NMOS DA S DB GA
M0 DA GA SA SA NMOS
M1 DB GA SB SB NMOS
M2 SA DA S S NMOS
M3 SB DA S S NMOS
.ends CASCODED_CMC_NMOS

.subckt CASCODED_CMC_PMOS_B DA GA DB S B
M0 DA GA SA B PMOS
M1 DB GA SB B PMOS
M2 SA DB S B PMOS
M3 SB DB S B PMOS
.ends CASCODED_CMC_PMOS_B

.subckt CASCODED_CMC_NMOS_B DA S DB GA B
M0 DA GA SA B NMOS
M1 DB GA SB B NMOS
M2 SA DA S B NMOS
M3 SB DA S B NMOS
.ends CASCODED_CMC_NMOS_B

* DP subckts
.subckt DP_NMOS  DA DB GA GB S
M0 DA GA S S NMOS
M1 DB GB S S NMOS
.ends DP_NMOS

.subckt DP_PMOS  DA DB GA GB S
M0 DA GA S S PMOS
M1 DB GB S S PMOS
.ends DP_PMOS

.subckt DP_NMOS_B  DA DB GA GB S B
M0 DA GA S B NMOS
M1 DB GB S B NMOS
.ends DP_NMOS_B

.subckt DP_PMOS_B  DA DB GA GB S B
M0 DA GA S B PMOS
M1 DB GB S B PMOS
.ends DP_PMOS_B

* DCL subckts
.subckt DCL_NMOS D S
M0 D D S S NMOS
.ends DCL_NMOS

.subckt DCL_PMOS D S
M0 D D S S PMOS
.ends DCL_PMOS

.subckt DCL_NMOS_B D S B
M0 D D S B NMOS
.ends DCL_NMOS_B

.subckt DCL_PMOS_B D S B
M0 D D S B PMOS
.ends DCL_PMOS_B

* 2_STAGE_INV subckts
.subckt 2_STAGE_INV B0_INV B0_BUF B0 VSS VDD
MM7 B0_BUF B0_INV VSS VSS NMOS
MM4 B0_INV B0 VSS VSS NMOS
MM6 B0_BUF B0_INV VDD VDD PMOS
MM5 B0_INV B0 VDD VDD PMOS
.ends 2_STAGE_INV
