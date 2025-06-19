#Testing implementation of simple fusion reactions at the pedestal
#Assumptions:
# temperature = 0.5 keV
# ionic deuterium density = 3e+20 #/m^3
# neutral deuterium density = 3e+16 #/m^3

[GlobalParams]
  potential_units = V
  use_moles = true
[]

[Mesh]
  #Sets up a 0D mesh with 1 element
  [geo]
    type = GeneratedMeshGenerator
    nx = 1
    dim = 1
  []
[]

#Defines the problem type, such as FE, eigen value problem, etc.
[Problem]
  type = FEProblem
[]

#User defined name for the variables.
#Other variable properties are defined here,
# such as family of shape function and variable order
# (the default family/order is Lagrange/First)
[Variables]
  [D+]
  []
  [em]
  []
  [D]
  []
[]

[AuxVariables]
  [D+_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [em_density]
    order = CONSTANT
    family = MONOMIAL
  []
  [D_density]
    order = CONSTANT
    family = MONOMIAL
  []

  #Reaction rates
  #[ionization_rate]
  #  order = CONSTANT
  #  family = MONOMIAL
  #[]
  #[recombination_rate]
  #  order = CONSTANT
  #  family = MONOMIAL
  #[]
[]

[Kernels]
  #Adds the time derivative for the variables
  [D+_time_derv]
    type = TimeDerivative
    variable = D+
  []
  [em_time_derv]
    type = TimeDerivative
    variable = em
  []
  [D_time_derv]
    type = TimeDerivative
    variable = D
  []
[]

[AuxKernels]
  [D+_density_aux]
    type = DensityMoles
    variable = D+_density
    density_log = D+
    #execute_on = 'LINEAR TIMESTEP_END'
    execute_on = 'LINEAR TIMESTEP_BEGIN'
  []
  [em_density_aux]
    type = DensityMoles
    variable = em_density
    density_log = em
    #execute_on = 'LINEAR TIMESTEP_END'
    execute_on = 'LINEAR TIMESTEP_BEGIN'
  []
  [D_density_aux]
    type = DensityMoles
    variable = D_density
    density_log = D
    #execute_on = 'LINEAR TIMESTEP_END'
    execute_on = 'LINEAR TIMESTEP_BEGIN'
  []

  #Reaction rates
  #[ionization_rate_aux]
  #  type = FunctionAux
  #  variable = ionization_rate
  #  #function = '6.022e23 * 10^(-6) * (-32.4802533034*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(0) + -0.05440669186583*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(0) + 0.09048888225109*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(0) + -0.04054078993576*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(0) + 0.008976513750477*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(0) + -0.001060334011186*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(0) + 6.846238436472e-05*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(0) + -2.242955329604e-06*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(0) + 2.890437688072e-08*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(0) + 14.2533239151*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(1) + -0.0359434716076*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(1) + -0.02014729121556*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(1) + 0.0103977361573*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(1) + -0.001771792153042*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(1) + 0.0001237467264294*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(1) + -3.130184159149e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(1) + -3.051994601527e-08*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(1) + 1.888148175469e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(1) + -6.632235026785*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(2) + 0.09255558353174*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(2) + -0.005580210154625*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(2) + -0.005902218748238*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(2) + 0.001295609806553*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(2) + -0.0001056721622588*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(2) + 4.646310029498e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(2) + -1.479612391848e-07*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(2) + 2.85225125832e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(2) + 2.059544135448*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(3) + -0.07562462086943*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(3) + 0.01519595967433*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(3) + 0.0005803498098354*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(3) + -0.0003527285012725*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(3) + 3.201533740322e-05*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(3) + -1.835196889733e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(3) + 9.474014343303e-08*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(3) + -2.342505583774e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(3) + -0.442537033141*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(4) + 0.02882634019199*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(4) + -0.00728577148505*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(4) + 0.0004643389885987*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(4) + 1.145700685235e-06*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(4) + 8.493662724988e-07*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(4) + -1.001032516512e-08*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(4) + -1.476839184318e-08*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(4) + 6.047700368169e-10*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(4) + 0.06309381861496*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(5) + -0.00578868653578*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(5) + 0.00150738295525*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(5) + -0.0001201550548662*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(5) + 6.574487543511e-06*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(5) + -9.678782818849e-07*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(5) + 5.176265845225e-08*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(5) + 1.29155167686e-09*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(5) + -9.685157340473e-11*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(5) + -0.005620091829261*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(6) + 0.000632910556804*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(6) + -0.0001527777697951*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(6) + 8.270124691336e-06*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(6) + 3.224101773605e-08*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(6) + 4.377402649057e-08*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(6) + -2.622921686955e-09*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(6) + -2.259663431436e-10*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(6) + 1.161438990709e-11*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(6) + 0.0002812016578355*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(7) + -3.564132950345e-05*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(7) + 7.222726811078e-06*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(7) + 1.433018694347e-07*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(7) + -1.097431215601e-07*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(7) + 7.789031791949e-09*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(7) + -4.197728680251e-10*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(7) + 3.032260338723e-11*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(7) + -8.911076930014e-13*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(7) + -6.011143453374e-06*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(8) + 8.089651265488e-07*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(8) + -1.186212683668e-07*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(8) + -2.381080756307e-08*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(8) + 6.271173694534e-09*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(8) + -5.48301024493e-10*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(8) + 3.064611702159e-11*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(8) + -1.355903284487e-12*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(8) + 2.935080031599e-14*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(8))'
  #  function = '6.022e23 * 10^(-6) * (-32.4802533034*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(0))'
  #  execute_on = 'LINEAR TIMESTEP_END'
  #[]
  #[recombination_rate_aux]
  #  type = FunctionAux
  #  variable = recombination_rate
  #  #function = '6.022e23 * 10^(-6) * (-28.58858570847*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(0) + 0.02068671746773*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(0) + -0.007868331504755*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(0) + 0.003843362133859*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(0) + -0.0007411492158905*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(0) + 9.273687892997e-05*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(0) + -7.063529824805e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(0) + 3.026539277057e-07*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(0) + -5.373940838104e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(0) + -0.7676413320499*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(1) + 0.0127800603259*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(1) + -0.01870326896978*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(1) + 0.00382855504889*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(1) + -0.0003627770385335*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(1) + 4.401007253801e-07*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(1) + 1.932701779173e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(1) + -1.176872895577e-07*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(1) + 2.215851843121e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(1) + 0.002823851790251*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(2) + -0.001907812518731*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(2) + 0.01121251125171*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(2) + -0.003711328186517*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(2) + 0.0006617485083301*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(2) + -6.860774445002e-05*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(2) + 4.508046989099e-06*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(2) + -1.723423509284e-07*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(2) + 2.805361431741e-09*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(2) + -0.01062884273731*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(3) + -0.01010719783828*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(3) + 0.004208412930611*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(3) + -0.00100574441054*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(3) + 0.0001013652422369*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(3) + -2.044691594727e-06*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(3) + -4.431181498017e-07*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(3) + 3.457903389784e-08*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(3) + -7.374639775683e-10*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(3) + 0.001582701550903*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(4) + 0.002794099401979*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(4) + -0.002024796037098*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(4) + 0.0006250304936976*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(4) + -9.224891301052e-05*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(4) + 7.546853961575e-06*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(4) + -3.682709551169e-07*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(4) + 1.035928615391e-08*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(4) + -1.325312585168e-10*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(4) + -0.0001938012790522*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(5) + 0.0002148453735781*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(5) + 3.393285358049e-05*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(5) + -3.746423753955e-05*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(5) + 7.509176112468e-06*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(5) + -8.688365258514e-07*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(5) + 7.144767938783e-08*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(5) + -3.367897014044e-09*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(5) + 6.250111099227e-11*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(5) + 6.041794354114e-06*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(6) + -0.0001421502819671*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(6) + 6.14387907608e-05*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(6) + -1.232549226121e-05*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(6) + 1.394562183496e-06*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(6) + -6.434833988001e-08*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(6) + -2.746804724917e-09*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(6) + 3.564291012995e-10*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(6) + -8.55170819761e-12*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(6) + 1.742316850715e-06*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(7) + 1.595051038326e-05*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(7) + -7.858419208668e-06*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(7) + 1.774935420144e-06*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(7) + -2.187584251561e-07*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(7) + 1.327090702659e-08*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(7) + -1.386720240985e-10*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(7) + -1.946206688519e-11*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(7) + 5.745422385081e-13*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(7) + -1.384927774988e-07*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(8) + -5.664673433879e-07*log((6.022e23*exp(em))/(10^14))^(1)*log(${Te})^(8) + 2.886857762387e-07*log((6.022e23*exp(em))/(10^14))^(2)*log(${Te})^(8) + -6.591743182569e-08*log((6.022e23*exp(em))/(10^14))^(3)*log(${Te})^(8) + 8.008790343319e-09*log((6.022e23*exp(em))/(10^14))^(4)*log(${Te})^(8) + -4.805837071646e-10*log((6.022e23*exp(em))/(10^14))^(5)*log(${Te})^(8) + 6.459706573699e-12*log((6.022e23*exp(em))/(10^14))^(6)*log(${Te})^(8) + 5.510729582791e-13*log((6.022e23*exp(em))/(10^14))^(7)*log(${Te})^(8) + -1.680871303639e-14*log((6.022e23*exp(em))/(10^14))^(8)*log(${Te})^(8))'
  #  function = '6.022e23 * 10^(-6) * (-28.58858570847*log((6.022e23*exp(em))/(10^14))^(0)*log(${Te})^(0))'
  #  execute_on = 'LINEAR TIMESTEP_END'
  #[]
[]


#Te = '500'

[Materials]
  [GasBasics]
    type = GasElectronMoments
    interp_elastic_coeff = false
    interp_trans_coeffs = false
    property_tables_file = ../rate_coefficients/electron_moments.txt
    ramp_trans_coeffs = false
    user_p_gas = 10000
  []
[]

#CRANE's Reactions Action that inputs the reactions as source terms for the variables
[Reactions]
  [Gas]
    #Name of each variable on the reactant side
    species = 'D+ em D'
    #Define type of coefficient (rate or townsend)
    reaction_coefficient_format = 'rate'
    #Define if using log form
    use_log = true
    #Define if using automatic differentiation
    use_ad = true
    #Define which material block the reactions take place.
    # For undefine blocks, naming starts at 0
    block = 0
    equation_constants = 'T_e'
    equation_values = '500'
    equation_variables = 'em_density'
    #Define reactions and coefficients
    reactions = 'em + D -> em + em + D+  : {6.022e23 * 10^(-6) * (-32.4802533034*log(em_density/(10^14))^(0)*log(T_e)^(0) + -0.05440669186583*log(em_density/(10^14))^(1)*log(T_e)^(0) + 0.09048888225109*log(em_density/(10^14))^(2)*log(T_e)^(0) + -0.04054078993576*log(em_density/(10^14))^(3)*log(T_e)^(0) + 0.008976513750477*log(em_density/(10^14))^(4)*log(T_e)^(0) + -0.001060334011186*log(em_density/(10^14))^(5)*log(T_e)^(0) + 6.846238436472e-05*log(em_density/(10^14))^(6)*log(T_e)^(0) + -2.242955329604e-06*log(em_density/(10^14))^(7)*log(T_e)^(0) + 2.890437688072e-08*log(em_density/(10^14))^(8)*log(T_e)^(0) + 14.2533239151*log(em_density/(10^14))^(0)*log(T_e)^(1) + -0.0359434716076*log(em_density/(10^14))^(1)*log(T_e)^(1) + -0.02014729121556*log(em_density/(10^14))^(2)*log(T_e)^(1) + 0.0103977361573*log(em_density/(10^14))^(3)*log(T_e)^(1) + -0.001771792153042*log(em_density/(10^14))^(4)*log(T_e)^(1) + 0.0001237467264294*log(em_density/(10^14))^(5)*log(T_e)^(1) + -3.130184159149e-06*log(em_density/(10^14))^(6)*log(T_e)^(1) + -3.051994601527e-08*log(em_density/(10^14))^(7)*log(T_e)^(1) + 1.888148175469e-09*log(em_density/(10^14))^(8)*log(T_e)^(1) + -6.632235026785*log(em_density/(10^14))^(0)*log(T_e)^(2) + 0.09255558353174*log(em_density/(10^14))^(1)*log(T_e)^(2) + -0.005580210154625*log(em_density/(10^14))^(2)*log(T_e)^(2) + -0.005902218748238*log(em_density/(10^14))^(3)*log(T_e)^(2) + 0.001295609806553*log(em_density/(10^14))^(4)*log(T_e)^(2) + -0.0001056721622588*log(em_density/(10^14))^(5)*log(T_e)^(2) + 4.646310029498e-06*log(em_density/(10^14))^(6)*log(T_e)^(2) + -1.479612391848e-07*log(em_density/(10^14))^(7)*log(T_e)^(2) + 2.85225125832e-09*log(em_density/(10^14))^(8)*log(T_e)^(2) + 2.059544135448*log(em_density/(10^14))^(0)*log(T_e)^(3) + -0.07562462086943*log(em_density/(10^14))^(1)*log(T_e)^(3) + 0.01519595967433*log(em_density/(10^14))^(2)*log(T_e)^(3) + 0.0005803498098354*log(em_density/(10^14))^(3)*log(T_e)^(3) + -0.0003527285012725*log(em_density/(10^14))^(4)*log(T_e)^(3) + 3.201533740322e-05*log(em_density/(10^14))^(5)*log(T_e)^(3) + -1.835196889733e-06*log(em_density/(10^14))^(6)*log(T_e)^(3) + 9.474014343303e-08*log(em_density/(10^14))^(7)*log(T_e)^(3) + -2.342505583774e-09*log(em_density/(10^14))^(8)*log(T_e)^(3) + -0.442537033141*log(em_density/(10^14))^(0)*log(T_e)^(4) + 0.02882634019199*log(em_density/(10^14))^(1)*log(T_e)^(4) + -0.00728577148505*log(em_density/(10^14))^(2)*log(T_e)^(4) + 0.0004643389885987*log(em_density/(10^14))^(3)*log(T_e)^(4) + 1.145700685235e-06*log(em_density/(10^14))^(4)*log(T_e)^(4) + 8.493662724988e-07*log(em_density/(10^14))^(5)*log(T_e)^(4) + -1.001032516512e-08*log(em_density/(10^14))^(6)*log(T_e)^(4) + -1.476839184318e-08*log(em_density/(10^14))^(7)*log(T_e)^(4) + 6.047700368169e-10*log(em_density/(10^14))^(8)*log(T_e)^(4) + 0.06309381861496*log(em_density/(10^14))^(0)*log(T_e)^(5) + -0.00578868653578*log(em_density/(10^14))^(1)*log(T_e)^(5) + 0.00150738295525*log(em_density/(10^14))^(2)*log(T_e)^(5) + -0.0001201550548662*log(em_density/(10^14))^(3)*log(T_e)^(5) + 6.574487543511e-06*log(em_density/(10^14))^(4)*log(T_e)^(5) + -9.678782818849e-07*log(em_density/(10^14))^(5)*log(T_e)^(5) + 5.176265845225e-08*log(em_density/(10^14))^(6)*log(T_e)^(5) + 1.29155167686e-09*log(em_density/(10^14))^(7)*log(T_e)^(5) + -9.685157340473e-11*log(em_density/(10^14))^(8)*log(T_e)^(5) + -0.005620091829261*log(em_density/(10^14))^(0)*log(T_e)^(6) + 0.000632910556804*log(em_density/(10^14))^(1)*log(T_e)^(6) + -0.0001527777697951*log(em_density/(10^14))^(2)*log(T_e)^(6) + 8.270124691336e-06*log(em_density/(10^14))^(3)*log(T_e)^(6) + 3.224101773605e-08*log(em_density/(10^14))^(4)*log(T_e)^(6) + 4.377402649057e-08*log(em_density/(10^14))^(5)*log(T_e)^(6) + -2.622921686955e-09*log(em_density/(10^14))^(6)*log(T_e)^(6) + -2.259663431436e-10*log(em_density/(10^14))^(7)*log(T_e)^(6) + 1.161438990709e-11*log(em_density/(10^14))^(8)*log(T_e)^(6) + 0.0002812016578355*log(em_density/(10^14))^(0)*log(T_e)^(7) + -3.564132950345e-05*log(em_density/(10^14))^(1)*log(T_e)^(7) + 7.222726811078e-06*log(em_density/(10^14))^(2)*log(T_e)^(7) + 1.433018694347e-07*log(em_density/(10^14))^(3)*log(T_e)^(7) + -1.097431215601e-07*log(em_density/(10^14))^(4)*log(T_e)^(7) + 7.789031791949e-09*log(em_density/(10^14))^(5)*log(T_e)^(7) + -4.197728680251e-10*log(em_density/(10^14))^(6)*log(T_e)^(7) + 3.032260338723e-11*log(em_density/(10^14))^(7)*log(T_e)^(7) + -8.911076930014e-13*log(em_density/(10^14))^(8)*log(T_e)^(7) + -6.011143453374e-06*log(em_density/(10^14))^(0)*log(T_e)^(8) + 8.089651265488e-07*log(em_density/(10^14))^(1)*log(T_e)^(8) + -1.186212683668e-07*log(em_density/(10^14))^(2)*log(T_e)^(8) + -2.381080756307e-08*log(em_density/(10^14))^(3)*log(T_e)^(8) + 6.271173694534e-09*log(em_density/(10^14))^(4)*log(T_e)^(8) + -5.48301024493e-10*log(em_density/(10^14))^(5)*log(T_e)^(8) + 3.064611702159e-11*log(em_density/(10^14))^(6)*log(T_e)^(8) + -1.355903284487e-12*log(em_density/(10^14))^(7)*log(T_e)^(8) + 2.935080031599e-14*log(em_density/(10^14))^(8)*log(T_e)^(8))}
                 D+ + em -> D            : {6.022e23 * 10^(-6) * (-28.58858570847*log(em_density/(10^14))^(0)*log(T_e)^(0) + 0.02068671746773*log(em_density/(10^14))^(1)*log(T_e)^(0) + -0.007868331504755*log(em_density/(10^14))^(2)*log(T_e)^(0) + 0.003843362133859*log(em_density/(10^14))^(3)*log(T_e)^(0) + -0.0007411492158905*log(em_density/(10^14))^(4)*log(T_e)^(0) + 9.273687892997e-05*log(em_density/(10^14))^(5)*log(T_e)^(0) + -7.063529824805e-06*log(em_density/(10^14))^(6)*log(T_e)^(0) + 3.026539277057e-07*log(em_density/(10^14))^(7)*log(T_e)^(0) + -5.373940838104e-09*log(em_density/(10^14))^(8)*log(T_e)^(0) + -0.7676413320499*log(em_density/(10^14))^(0)*log(T_e)^(1) + 0.0127800603259*log(em_density/(10^14))^(1)*log(T_e)^(1) + -0.01870326896978*log(em_density/(10^14))^(2)*log(T_e)^(1) + 0.00382855504889*log(em_density/(10^14))^(3)*log(T_e)^(1) + -0.0003627770385335*log(em_density/(10^14))^(4)*log(T_e)^(1) + 4.401007253801e-07*log(em_density/(10^14))^(5)*log(T_e)^(1) + 1.932701779173e-06*log(em_density/(10^14))^(6)*log(T_e)^(1) + -1.176872895577e-07*log(em_density/(10^14))^(7)*log(T_e)^(1) + 2.215851843121e-09*log(em_density/(10^14))^(8)*log(T_e)^(1) + 0.002823851790251*log(em_density/(10^14))^(0)*log(T_e)^(2) + -0.001907812518731*log(em_density/(10^14))^(1)*log(T_e)^(2) + 0.01121251125171*log(em_density/(10^14))^(2)*log(T_e)^(2) + -0.003711328186517*log(em_density/(10^14))^(3)*log(T_e)^(2) + 0.0006617485083301*log(em_density/(10^14))^(4)*log(T_e)^(2) + -6.860774445002e-05*log(em_density/(10^14))^(5)*log(T_e)^(2) + 4.508046989099e-06*log(em_density/(10^14))^(6)*log(T_e)^(2) + -1.723423509284e-07*log(em_density/(10^14))^(7)*log(T_e)^(2) + 2.805361431741e-09*log(em_density/(10^14))^(8)*log(T_e)^(2) + -0.01062884273731*log(em_density/(10^14))^(0)*log(T_e)^(3) + -0.01010719783828*log(em_density/(10^14))^(1)*log(T_e)^(3) + 0.004208412930611*log(em_density/(10^14))^(2)*log(T_e)^(3) + -0.00100574441054*log(em_density/(10^14))^(3)*log(T_e)^(3) + 0.0001013652422369*log(em_density/(10^14))^(4)*log(T_e)^(3) + -2.044691594727e-06*log(em_density/(10^14))^(5)*log(T_e)^(3) + -4.431181498017e-07*log(em_density/(10^14))^(6)*log(T_e)^(3) + 3.457903389784e-08*log(em_density/(10^14))^(7)*log(T_e)^(3) + -7.374639775683e-10*log(em_density/(10^14))^(8)*log(T_e)^(3) + 0.001582701550903*log(em_density/(10^14))^(0)*log(T_e)^(4) + 0.002794099401979*log(em_density/(10^14))^(1)*log(T_e)^(4) + -0.002024796037098*log(em_density/(10^14))^(2)*log(T_e)^(4) + 0.0006250304936976*log(em_density/(10^14))^(3)*log(T_e)^(4) + -9.224891301052e-05*log(em_density/(10^14))^(4)*log(T_e)^(4) + 7.546853961575e-06*log(em_density/(10^14))^(5)*log(T_e)^(4) + -3.682709551169e-07*log(em_density/(10^14))^(6)*log(T_e)^(4) + 1.035928615391e-08*log(em_density/(10^14))^(7)*log(T_e)^(4) + -1.325312585168e-10*log(em_density/(10^14))^(8)*log(T_e)^(4) + -0.0001938012790522*log(em_density/(10^14))^(0)*log(T_e)^(5) + 0.0002148453735781*log(em_density/(10^14))^(1)*log(T_e)^(5) + 3.393285358049e-05*log(em_density/(10^14))^(2)*log(T_e)^(5) + -3.746423753955e-05*log(em_density/(10^14))^(3)*log(T_e)^(5) + 7.509176112468e-06*log(em_density/(10^14))^(4)*log(T_e)^(5) + -8.688365258514e-07*log(em_density/(10^14))^(5)*log(T_e)^(5) + 7.144767938783e-08*log(em_density/(10^14))^(6)*log(T_e)^(5) + -3.367897014044e-09*log(em_density/(10^14))^(7)*log(T_e)^(5) + 6.250111099227e-11*log(em_density/(10^14))^(8)*log(T_e)^(5) + 6.041794354114e-06*log(em_density/(10^14))^(0)*log(T_e)^(6) + -0.0001421502819671*log(em_density/(10^14))^(1)*log(T_e)^(6) + 6.14387907608e-05*log(em_density/(10^14))^(2)*log(T_e)^(6) + -1.232549226121e-05*log(em_density/(10^14))^(3)*log(T_e)^(6) + 1.394562183496e-06*log(em_density/(10^14))^(4)*log(T_e)^(6) + -6.434833988001e-08*log(em_density/(10^14))^(5)*log(T_e)^(6) + -2.746804724917e-09*log(em_density/(10^14))^(6)*log(T_e)^(6) + 3.564291012995e-10*log(em_density/(10^14))^(7)*log(T_e)^(6) + -8.55170819761e-12*log(em_density/(10^14))^(8)*log(T_e)^(6) + 1.742316850715e-06*log(em_density/(10^14))^(0)*log(T_e)^(7) + 1.595051038326e-05*log(em_density/(10^14))^(1)*log(T_e)^(7) + -7.858419208668e-06*log(em_density/(10^14))^(2)*log(T_e)^(7) + 1.774935420144e-06*log(em_density/(10^14))^(3)*log(T_e)^(7) + -2.187584251561e-07*log(em_density/(10^14))^(4)*log(T_e)^(7) + 1.327090702659e-08*log(em_density/(10^14))^(5)*log(T_e)^(7) + -1.386720240985e-10*log(em_density/(10^14))^(6)*log(T_e)^(7) + -1.946206688519e-11*log(em_density/(10^14))^(7)*log(T_e)^(7) + 5.745422385081e-13*log(em_density/(10^14))^(8)*log(T_e)^(7) + -1.384927774988e-07*log(em_density/(10^14))^(0)*log(T_e)^(8) + -5.664673433879e-07*log(em_density/(10^14))^(1)*log(T_e)^(8) + 2.886857762387e-07*log(em_density/(10^14))^(2)*log(T_e)^(8) + -6.591743182569e-08*log(em_density/(10^14))^(3)*log(T_e)^(8) + 8.008790343319e-09*log(em_density/(10^14))^(4)*log(T_e)^(8) + -4.805837071646e-10*log(em_density/(10^14))^(5)*log(T_e)^(8) + 6.459706573699e-12*log(em_density/(10^14))^(6)*log(T_e)^(8) + 5.510729582791e-13*log(em_density/(10^14))^(7)*log(T_e)^(8) + -1.680871303639e-14*log(em_density/(10^14))^(8)*log(T_e)^(8))}'
  []
[]

#Initial conditions for variables.More actions
#If left undefine, the IC is zero
[ICs]
  [D+_ic]
    type = FunctionIC
    variable = D+
    function = 'log(1e+16/6.022e+23)'
  []
  [em_ic]
    type = FunctionIC
    variable = em
    function = 'log(1e+16/6.022e+23)'
  []
  [D_ic]
    type = FunctionIC
    variable = D
    function = 'log(1e+20/6.022e+23)'
  []
[]

#Preconditioning options
#Learn more at: https://mooseframework.inl.gov/syntax/Preconditioning/index.html
[Preconditioning]
  active = 'smp'
  [smp]
    type = SMP
    full = true
  []

  [fdp]
    type = FDP
    full = true
  []
[]

#How to execute the problem.
#Defines type of solve (such as steady or transient),
# solve type (Newton, PJFNK, etc.) and tolerances
[Executioner]
  type = Transient
  end_time = 1.06249e-6
  dt = 1e-9
  dtmin = 1e-14
  scheme = bdf2
  #solve_type = NEWTON
  solve_type = PJFNK
  steady_state_detection = true

  petsc_options = '-snes_converged_reason -snes_linesearch_monitor'
  petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_shift_amount -snes_linesearch_minlambda'
  petsc_options_value = 'lu NONZERO 1.e-10 1e-3'

  nl_rel_tol = 1e-08
  l_max_its = 20
[]

#Defines the output type of the file (multiple output files can be define per run)
[Outputs]
  perf_graph = true
  [out]
    type = Exodus
  []
[]
