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
    execute_on = 'LINEAR TIMESTEP_END'
  []
  [em_density_aux]
    type = DensityMoles
    variable = em_density
    density_log = em
    execute_on = 'LINEAR TIMESTEP_END'
  []
  [D_density_aux]
    type = DensityMoles
    variable = D_density
    density_log = D
    execute_on = 'LINEAR TIMESTEP_END'
  []
[]

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
    #Define reactions and coefficients
    reactions = 'em + D -> em + em + D+  : 2.5856251254792084e+10
                 D+ + em -> D            : 5.364987086029923e+2'
  []
[]

#Initial conditions for variables.More actions
#If left undefine, the IC is zero
[ICs]
  [D+_ic]
    type = FunctionIC
    variable = D+
    function = 'log(3e14/6.022e+23)'
  []
  [em_ic]
    type = FunctionIC
    variable = em
    function = 'log(3e14/6.022e+23)'
  []
  [D_ic]
    type = FunctionIC
    variable = D
    function = 'log(3e+20/6.022e+23)'
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
  end_time = 4e+3
  dt = 1e+0
  dtmin = 1e-14
  scheme = bdf2
  solve_type = NEWTON
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