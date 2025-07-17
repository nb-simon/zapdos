#script for analyzing the behavior of the full reaction network
#based on CRANE's "Two-Reaction Argon Plasma" tutorial

##import
#import numpy for reading .txt file
import numpy as np

#import matplotlib for visualization
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})

import math

##electron temperature
T_e = 500

##verification data
#atomic ratio fit
a_ratio = [
  [-3.885296435411E+00, -5.697204983970E-02, 7.332383617797E-02, -3.505183129037E-02, 8.175768579910E-03, -1.025860190568E-03, 7.041006112962E-05, -2.467291455100E-06, 3.436102553376E-08],
  [1.505487187018E+01, 4.633572829771E-04, -1.702732444633E-03, 1.882868187070E-03, -6.728098565933E-04, 1.133241004935E-04, -9.735191629933E-06, 4.053170686858E-07, -6.463282471161E-09],
  [-6.749191912028E+00, 1.050145613783E-03, -3.148776304951E-03, 1.594704172137E-03, -3.246647453262E-04, 3.184754694533E-05, -1.387656614654E-06, 1.600623293301E-08, 2.722493472041E-10],
  [2.212221660002E+00, 4.854461323593E-03, -2.452783916892E-03, 4.064257852894E-04, -2.059459670150E-05, -2.358171220598E-06, 3.488698891258E-07, -1.422059161908E-08, 1.698254518458E-10],
  [-5.257981277508E-01, -3.179654723425E-03, 1.767567981601E-03, -3.839001285389E-04, 4.783673711689E-05, -3.378269018931E-06, 9.511636577030E-08, 6.913540712148E-10, -5.483090178167E-11],
  [8.824411449640E-02, 9.193475524397E-04, -4.299802583958E-04, 6.248027250326E-05, -4.077787495573E-06, 1.124935475483E-07, 1.140116701448E-08, -1.211498169926E-09, 3.020216342872E-11],
  [-9.799369577387E-03, -1.679454700153E-04, 7.381643118061E-05, -7.865967145477E-06, -4.674862715791E-08, 4.744742742259E-08, -4.127705769609E-09, 2.185243304602E-10, -4.848384547542E-12],
  [6.413937652029E-04, 1.902440743752E-05, -9.875692439849E-06, 1.734207080274E-06, -1.760833256154E-07, 1.551629723045E-08, -9.432683181108E-10, 2.682232500047E-11, -2.216051536502E-13],
  [-1.861114574375E-05, -9.394367819466E-07, 5.893327001637E-07, -1.457328885095E-07, 2.193301182972E-08, -2.248254389232E-09, 1.398963108397E-10, -4.493865381320E-12, 5.590467018306E-14],
]

#molecular ratio fit
m_ratio = [
  [-1.929803964240E+01, 2.097006502950E-01, -1.100904809661E-01, 4.477781641551E-02, -9.060826089295E-03, 1.170547725039E-03, -8.893455666588E-05, 3.479454987799E-06, -5.361512296401E-08],
  [1.727612905933E+01, -4.662670859833E-01, 8.567341672326E-02, -6.827368520293E-03, -3.618060467670E-03, 6.852659500488E-04, -4.473404420068E-05, 1.209602016239E-06, -1.069974187479E-08],
  [-8.438025952533E+00, 6.115179297110E-01, -1.153478632323E-01, 1.993457166448E-02, 1.643837202714E-04, -3.516424328964E-04, 3.207886028645E-05, -1.101305933603E-06, 1.299192188737E-08],
  [2.883389908864E+00, -4.286361930144E-01, 6.596018559458E-02, -1.341784022457E-02, 1.582201264314E-03, -7.056994955968E-05, 4.431489645883E-07, 2.326874797653E-08, 1.068518137706E-10],
  [-7.403401021470E-01, 1.809442086665E-01, -1.864042138902E-02, 1.875666968084E-03, -2.978688155916E-04, 2.721069163086E-05, -1.428413713222E-06, 4.845148645034E-08, -8.048035605554E-10],
  [1.387371448471E-01, -4.879175895909E-02, 4.430141421894E-03, 1.476743155802E-04, -3.955049388000E-05, 2.382368688632E-06, -5.790867265229E-08, -6.986008432331E-10, 4.535659079263E-11],
  [-1.746217632264E-02, 8.151856339270E-03, -1.015594807894E-03, 6.205132641268E-06, 7.210178682186E-06, -6.812476857444E-07, 3.277446170025E-08, -8.583517963518E-10, 9.700723935742E-12],
  [1.287561948974E-03, -7.544209459715E-04, 1.374937928555E-04, -1.222677896703E-05, 8.247029259344E-07, -5.043186962921E-08, 2.025920058300E-09, -3.655728430701E-11, 8.337869178540E-14],
  [-4.136061327089E-05, 2.914443517923E-05, -7.106408217685E-06, 1.041267499432E-06, -1.158374992604E-07, 9.052478729563E-09, -4.280094258996E-10, 1.063115935764E-11, -1.030790224273E-13],
]
#AMJUEL H.4 Reaction 2.1.5: H + e --> H+ + 2e
coeffsEI1 = [
  [-3.248025330340E+01, -5.440669186583E-02, 9.048888225109E-02, -4.054078993576E-02, 8.976513750477E-03, -1.060334011186E-03, 6.846238436472E-05, -2.242955329604E-06, 2.890437688072E-08],
  [1.425332391510E+01, -3.594347160760E-02, -2.014729121556E-02, 1.039773615730E-02, -1.771792153042E-03, 1.237467264294E-04, -3.130184159149E-06, -3.051994601527E-08, 1.888148175469E-09],
  [-6.632235026785E+00, 9.255558353174E-02, -5.580210154625E-03, -5.902218748238E-03, 1.295609806553E-03, -1.056721622588E-04, 4.646310029498E-06, -1.479612391848E-07, 2.852251258320E-09],
  [2.059544135448E+00, -7.562462086943E-02, 1.519595967433E-02, 5.803498098354E-04, -3.527285012725E-04, 3.201533740322E-05, -1.835196889733E-06, 9.474014343303E-08, -2.342505583774E-09],
  [-4.425370331410E-01, 2.882634019199E-02, -7.285771485050E-03, 4.643389885987E-04, 1.145700685235E-06, 8.493662724988E-07, -1.001032516512E-08, -1.476839184318E-08, 6.047700368169E-10],
  [6.309381861496E-02, -5.788686535780E-03, 1.507382955250E-03, -1.201550548662E-04, 6.574487543511E-06, -9.678782818849E-07, 5.176265845225E-08, 1.291551676860E-09, -9.685157340473E-11],
  [-5.620091829261E-03, 6.329105568040E-04, -1.527777697951E-04, 8.270124691336E-06, 3.224101773605E-08, 4.377402649057E-08, -2.622921686955E-09, -2.259663431436E-10, 1.161438990709E-11],
  [2.812016578355E-04, -3.564132950345E-05, 7.222726811078E-06, 1.433018694347E-07, -1.097431215601E-07, 7.789031791949E-09, -4.197728680251E-10, 3.032260338723E-11, -8.911076930014E-13],
  [-6.011143453374E-06, 8.089651265488E-07, -1.186212683668E-07, -2.381080756307E-08, 6.271173694534E-09, -5.483010244930E-10, 3.064611702159E-11, -1.355903284487E-12, 2.935080031599E-14],
]

#AMJUEL H.4 Reaction 2.2.9: e + H2 --> 2e + H2+
coeffsEI2 = [
  [-3.574773783577E+01, 3.470247049909E-01, -9.683166540937E-02, 1.959576276250E-03, 2.479361119190E-03, -1.196632952666E-04, -1.862956119592E-05, 1.669867158509E-06, -3.673736278200E-08],
  [1.769208985507E+01, -1.311169841222E+00, 4.700486215943E-01, -5.521175478827E-02, -2.689651616933E-03, 7.308915874002E-04, -2.920560755694E-05, -3.148831240316E-07, 2.514856386324E-08],
  [-8.291764008409E+00, 1.591701525694E+00, -5.814996025336E-01, 9.160898084105E-02, -4.770789631868E-03, 1.994775632224E-05, -7.511552245648E-06, 1.089689676313E-06, -2.920863498031E-08],
  [2.555712347240E+00, -8.625268584825E-01, 2.612076696684E-01, -3.686525285376E-02, 1.945480608139E-03, -3.690918356665E-05, 4.836340453567E-06, -4.165748666929E-07, 9.265898224345E-09],
  [-5.370404654062E-01, 2.375816996323E-01, -4.165908778170E-02, 1.732469114063E-03, 3.693513203529E-04, -4.931268184607E-05, 2.727501534044E-06, -1.081027384449E-07, 2.420509440644E-09],
  [7.443307905391E-02, -3.322214182214E-02, -2.351235556666E-03, 1.723053881691E-03, -2.096625925098E-04, 1.358575558294E-05, -1.041586202167E-06, 6.928574330531E-08, -1.746656185835E-09],
  [-6.391785721973E-03, 1.862554278190E-03, 1.540632467396E-03, -3.547150770477E-04, 1.392157055273E-05, 1.047463944093E-06, 1.513510667993E-08, -9.915499708242E-09, 3.298173891188E-10],
  [3.001729098239E-04, 3.497202259366E-05, -1.742029226138E-04, 2.296551698214E-05, 2.357520372192E-06, -5.306085513950E-07, 2.223137028418E-08, 3.340169309800E-10, -2.560542889504E-11],
  [-5.607182991432E-06, -5.779550092391E-06, 6.495742927455E-06, -3.040011333889E-07, -2.361542565281E-07, 3.655056080262E-08, -1.771478792301E-09, 1.334615260635E-11, 6.831564719957E-13],
]

#AMJUEL H.4 Reaction 2.2.11: e + H2+ --> 2e + H+ + H+
coeffsEI3 = [
  [-3.708803769397E+01, 9.784233987341E-02, -7.200361272130E-03, 6.496843022778E-03, -1.420590818760E-03, 1.703620321164E-04, -1.160738946400E-05, 4.148222302162E-07, -6.007853385325E-09],
  [1.561780529774E+01, -1.673256230592E-02, 2.743322772895E-02, -1.026956102747E-02, 1.999561527383E-03, -2.043607814503E-04, 1.084177127603E-05, -2.671800995803E-07, 2.093182411476E-09],
  [-6.874406034117E+00, -7.782929961315E-03, -6.888773684846E-03, 2.306107197863E-03, -4.029222834436E-04, 3.932152471491E-05, -2.094907364150E-06, 5.682907060010E-08, -6.320752545610E-10],
  [2.010540060675E+00, -3.226785148562E-03, -6.181192193854E-03, 2.388146990238E-03, -5.018901320009E-04, 5.520233512352E-05, -3.080798536641E-06, 7.864770315002E-08, -6.357395371638E-10],
  [-3.614768906120E-01, 3.710098881765E-03, 2.045814599796E-03, -8.523935993991E-04, 1.751295192861E-04, -1.944203941844E-05, 1.138888354831E-06, -3.256303793266E-08, 3.501794038444E-10],
  [2.956861321735E-02, -5.524443504504E-04, -2.457951062112E-05, 3.433179945503E-05, -1.450208898992E-06, -2.447566480782E-07, 1.375679100044E-08, 4.863880510459E-10, -3.004374374556E-11],
  [9.662490252868E-04, -1.548556801431E-04, 1.417215042439E-05, -6.444863591678E-06, -1.566028729499E-06, 4.152486680818E-07, -2.855068942744E-08, 6.081804811000E-10, 9.512865901179E-13],
  [-3.543571865464E-04, 4.662969089421E-05, -1.471117766355E-05, 5.235585096328E-06, -5.779667826854E-07, 2.139729421817E-08, -3.656048425230E-10, 3.759866326965E-11, -1.486151370215E-12],
  [1.827109843671E-05, -3.179895716088E-06, 1.432429412413E-06, -5.141065080107E-07, 7.734387173369E-08, -6.163336831045E-09, 3.128313515842E-10, -1.061842444216E-11, 1.771099769640E-13],
]

#AMJUEL H.4 Reaction 2.2.5g: e + H2 --> e + H + H
coeffsDS1 = [
  [-2.702372540584E+01, -3.152103191633E-03, 5.990692171729E-03, -3.151252835426E-03, 7.457309144890E-04, -9.238664007853E-05, 6.222557542845E-06, -2.160024578659E-07, 3.028755759836E-09],
  [1.081756417479E+01, -1.487216964825E-02, 1.417396532101E-02, -4.689911797083E-03, 7.180338663163E-04, -5.502798587526E-05, 1.983066081752E-06, -2.207639762507E-08, -2.116339335271E-10],
  [-5.368872027676E+00, 5.419787589654E-03, -1.747268613395E-02, 9.532963297450E-03, -2.196705622859E-03, 2.611447288152E-04, -1.695536960581E-05, 5.737375510694E-07, -7.940900078995E-09],
  [1.340684229143E+00, 1.058157580038E-02, -3.446019122786E-03, -7.032769815599E-04, 4.427959286553E-04, -7.370484189164E-05, 5.746786010618E-06, -2.182085196303E-07, 3.264045809897E-09],
  [-1.561644923145E-01, -3.847438570333E-03, 3.571477356851E-03, -1.103305795473E-03, 1.476712517858E-04, -8.461162952132E-06, 9.757111870171E-08, 8.130014050833E-09, -2.234996157750E-10],
  [-1.444731533894E-04, -3.194532513126E-04, -2.987368098475E-04, 2.092094838648E-04, -4.339352509941E-05, 4.009328699469E-06, -1.762651912129E-07, 3.357860444624E-09, -1.857322587267E-11],
  [2.117693926546E-03, 2.679309814780E-04, -1.037559373832E-04, 7.297053580368E-06, 1.454171585421E-06, -2.251616910293E-07, 9.191700327811E-09, -2.052366968228E-11, -3.567738654108E-12],
  [-2.143738340207E-04, -3.539232757385E-05, 1.909399233821E-05, -3.819368125069E-06, 3.754063159414E-07, -2.441872829462E-08, 1.437490161488E-09, -6.172308568891E-11, 1.104905484620E-12],
  [6.979740947331E-06, 1.462031952352E-06, -8.858634506391E-07, 2.099830142707E-07, -2.606862169776E-08, 2.039813579349E-09, -1.113483084607E-10, 3.859777100010E-12, -5.909099891913E-14],
]

#AMJUEL H.4 Reaction 2.2.10: e + H2 --> 2e + H + H+
coeffsDS2 = [
  [-3.793749300315E+01, -3.333162972531E-01, 1.849601203843E-01, -8.803945197107E-02, 2.205180180735E-02, -2.852568161901E-03, 1.942314738448E-04, -6.597388255594E-06, 8.798544848606E-08],
  [1.280249398154E+01, 1.028969438485E+00, -3.271855492638E-01, 1.305597441611E-01, -3.408439821910E-02, 4.591924060066E-03, -3.167471002157E-04, 1.070920193931E-05, -1.408139742113E-07],
  [-3.778148553140E+00, -1.415561059533E+00, 2.928509524911E-01, -7.425165688158E-02, 2.028424685287E-02, -3.042376564749E-03, 2.279124955373E-04, -8.197224564797E-06, 1.130682076163E-07],
  [2.499987501522E-01, 1.032922656537E+00, -1.580288004759E-01, 9.934702707539E-03, -2.450845732158E-03, 5.716646876513E-04, -5.339115778704E-05, 2.135848413694E-06, -3.072223247387E-08],
  [2.480574522949E-01, -4.372934216955E-01, 6.448433196301E-02, 1.229222932630E-03, -9.281410519553E-04, 5.946235618034E-05, -8.758032156912E-08, -7.270955072707E-08, 1.100087131523E-09],
  [-9.960628182831E-02, 1.092652428162E-01, -1.782307798975E-02, 1.192181214757E-04, 2.310636556641E-04, -2.492990725967E-05, 1.217600444191E-06, -3.624263301602E-08, 6.139167092128E-10],
  [1.709129400742E-02, -1.574889001363E-02, 2.865310743302E-03, -1.700396064727E-04, -1.502644504654E-06, 3.297869416435E-07, 6.572135289627E-10, 4.269190108005E-10, -3.666090917669E-11],
  [-1.435304503973E-03, 1.203823111704E-03, -2.350465388313E-04, 2.507288189894E-05, -3.077975735212E-06, 3.748299687254E-07, -2.613600078122E-08, 8.263175463927E-10, -8.509179497022E-12],
  [4.808639828229E-05, -3.761591649539E-05, 7.490531472388E-06, -1.077314971617E-06, 1.950247963978E-07, -2.569729600929E-08, 1.804377780165E-09, -6.031847199601E-11, 7.416020205748E-13],
]

#AMJUEL H.4 Reaction 2.2.12: e + H2+ --> e + H + H+
coeffsDS3 = [
  [-1.793443274600E+01, -4.932783688604E-02, 1.039088280849E-01, -4.375935166008E-02, 9.196691651936E-03, -1.043378648769E-03, 6.600342421838E-05, -2.198466460165E-06, 3.004145701249E-08],
  [2.236108757681E+00, -2.545406018621E-02, -1.160421006835E-01, 4.407846563362E-02, -8.192521304984E-03, 8.200277386433E-04, -4.508284363534E-05, 1.282824614809E-06, -1.474719350236E-08],
  [-3.620018994703E-01, 6.721527680150E-02, 1.564387124002E-02, -4.939045440424E-03, 4.263195867947E-04, 1.034216805418E-05, -3.975028601900E-06, 2.322116289258E-07, -4.381217154470E-09],
  [-4.353922258965E-01, -3.051033606589E-02, 3.512861172521E-02, -1.179504564265E-02, 2.091772760029E-03, -1.991100044575E-04, 1.018080238045E-05, -2.597941866088E-07, 2.524118386011E-09],
  [1.580381801957E-01, 2.493654957203E-03, -1.601970998119E-02, 5.346709597939E-03, -8.711870134835E-04, 7.542066727545E-05, -3.410778344979E-06, 7.120460603822E-08, -4.412295474522E-10],
  [1.697880687685E-02, 2.106675963900E-03, 4.521983358170E-04, -3.017151690655E-04, 6.209239389357E-05, -7.598119096817E-06, 5.523273241689E-07, -2.130508249251E-08, 3.319099650589E-10],
  [-1.521914651109E-02, -7.527862162788E-04, 9.095551479381E-04, -2.372576223034E-04, 3.018561480848E-05, -1.365255868731E-06, -4.604769733903E-08, 5.867910270430E-09, -1.357779142836E-10],
  [2.406276368070E-03, 9.971361856278E-05, -1.760978402353E-04, 4.877659148871E-05, -6.477358351729E-06, 3.541106430252E-07, 1.309772899670E-09, -8.072907334230E-10, 2.074669430611E-11],
  [-1.219469579955E-04, -4.785505675232E-06, 9.858840337511E-06, -2.779210878533E-06, 3.720379996058E-07, -2.110289928486E-08, 3.753875073646E-11, 4.024906665497E-11, -1.075990572574E-12],
]

#AMJUEL H.4 Reaction 2.2.14: e + H2+ --> H + H
coeffsDS4 = [
  [-1.664335253647E+01, 8.953780953631E-02, -1.056411030518E-01, 4.477000808690E-02, -9.729945434357E-03, 1.174456882002E-03, -7.987743820637E-05, 2.842957892768E-06, -4.104508608435E-08],
  [-6.005444031657E-01, 4.063933992726E-02, -4.753947846841E-02, 2.188304031377E-02, -5.201085606791E-03, 6.866340394051E-04, -5.059940013116E-05, 1.930213882205E-06, -2.963966822809E-08],
  [4.494812032769E-04, 7.884508616595E-05, 3.688007562485E-04, -4.659255785539E-04, 1.907115980400E-04, -3.434324710145E-05, 3.067651560323E-06, -1.325689465590E-07, 2.212493073620E-09],
  [1.632894866655E-04, 3.108116177617E-04, -3.521552580917E-04, -2.233169775063E-04, 1.869415236037E-04, -4.329991211511E-05, 4.465256901322E-06, -2.136296167564E-07, 3.873085368404E-09],
  [-7.234142549752E-05, -1.316311320262E-03, 1.643509328764E-03, -6.412764282779E-04, 1.048891053765E-04, -7.018555173322E-06, 4.776213235854E-08, 1.380537343974E-08, -4.199397846492E-10],
  [-1.504085050039E-05, 1.315865970237E-04, -1.025653773999E-04, 5.310324781249E-05, -1.831888048039E-05, 3.423755373077E-06, -3.303384352061E-07, 1.551627097700E-08, -2.809391819541E-10],
  [1.113923667684E-05, 2.711411525392E-05, -8.495922363727E-05, 4.026487801017E-05, -6.289324474240E-06, 1.911447036702E-07, 3.638198230235E-08, -3.235540606394E-09, 7.605442050634E-11],
  [-1.843926162250E-06, -1.663674537499E-06, 1.308069926896E-05, -7.324021449032E-06, 1.431739868187E-06, -1.085644779665E-07, 1.143164983367E-09, 2.151595003971E-10, -7.052562220005E-12],
  [9.864173150662E-08, -2.212261708468E-07, -4.431749501051E-07, 3.270530731011E-07, -7.282085521177E-08, 6.578253567957E-09, -1.925258267827E-10, -4.217474167519E-12, 2.364754029318E-13],
]

#AMJUEL H.4 Reaction 2.1.8: H+ + e --> H
coeffsRC = [
  [-2.858858570847E+01, 2.068671746773E-02, -7.868331504755E-03, 3.843362133859E-03, -7.411492158905E-04, 9.273687892997E-05, -7.063529824805E-06, 3.026539277057E-07, -5.373940838104E-09],
  [-7.676413320499E-01, 1.278006032590E-02, -1.870326896978E-02, 3.828555048890E-03, -3.627770385335E-04, 4.401007253801E-07, 1.932701779173E-06, -1.176872895577E-07, 2.215851843121E-09],
  [ 2.823851790251E-03, -1.907812518731E-03, 1.121251125171E-02, -3.711328186517E-03, 6.617485083301E-04, -6.860774445002E-05, 4.508046989099E-06, -1.723423509284E-07, 2.805361431741E-09],
  [-1.062884273731E-02, -1.010719783828E-02, 4.208412930611E-03, -1.005744410540E-03, 1.013652422369E-04, -2.044691594727E-06, -4.431181498017E-07, 3.457903389784E-08, -7.374639775683E-10],
  [1.582701550903E-03, 2.794099401979E-03, -2.024796037098E-03, 6.250304936976E-04, -9.224891301052E-05, 7.546853961575E-06, -3.682709551169E-07, 1.035928615391E-08, -1.325312585168E-10],
  [-1.938012790522E-04, 2.148453735781E-04, 3.393285358049E-05, -3.746423753955E-05, 7.509176112468E-06, -8.688365258514E-07, 7.144767938783E-08, -3.367897014044E-09, 6.250111099227E-11],
  [ 6.041794354114E-06, -1.421502819671E-04, 6.143879076080E-05, -1.232549226121E-05, 1.394562183496E-06, -6.434833988001E-08, -2.746804724917E-09, 3.564291012995E-10, -8.551708197610E-12],
  [1.742316850715E-06, 1.595051038326E-05, -7.858419208668E-06, 1.774935420144E-06, -2.187584251561E-07, 1.327090702659E-08, -1.386720240985E-10, -1.946206688519E-11, 5.745422385081E-13],
  [-1.384927774988E-07, -5.664673433879E-07, 2.886857762387E-07, -6.591743182569E-08, 8.008790343319E-09, -4.805837071646E-10, 6.459706573699E-12, 5.510729582791E-13, -1.680871303639E-14],
]

###working case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I120-I22.4e12-N116-N24e12.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select D2 density column
n_D2 = data[1:,1] # m^-3

#select D2+ density column
n_D2p = data[1:,2] # m^-3

#select D density column
n_D = data[1:,3] # m^-3

#select D+ density column
n_Dp = data[1:,4] # m^-3

#select electron density column
n_e = data[1:,20] # m^-3

#select dissociation rate 1 column
RDS1 = data[1:,5] # m^-3 s^-1

#select dissociation rate 2 column
RDS2 = data[1:,6] # m^-3 s^-1

#select dissociation rate 3 column
RDS3 = data[1:,7] # m^-3 s^-1

#select dissociation rate 4 column
RDS4 = data[1:,8] # m^-3 s^-1

#select ionization rate 1 column
REI1 = data[1:,9] # m^-3 s^-1

#select ionization rate 2 column
REI2 = data[1:,10] # m^-3 s^-1

#select ionization rate 3 column
REI3 = data[1:,11] # m^-3 s^-1

#select fusion rate 1 column
RFS1 = data[1:,12] # m^-3 s^-1

#select recombination rate column
RRC = data[1:,13] # m^-3 s^-1

#select D source column
SD = data[1:,14] # m^-3 s^-1

#select D2 source column
SD2 = data[1:,15] # m^-3 s^-1

#select D2+ source column
SD2p = data[1:,16] # m^-3 s^-1

#select D+ source column
SDp = data[1:,17] # m^-3 s^-1

#select electron source column
Sem = data[1:,18] # m^-3 s^-1

#select T+ density column
n_Tp = data[1:,19] #m^-3 s^-1

#select dissociation rate coefficient 1 column
kDS1 = data[1:,21] # m^3 s^-1

#select dissociation rate coefficient 2 column
kDS2 = data[1:,22] # m^3 s^-1

#select dissociation rate coefficient 3 column
kDS3 = data[1:,23] # m^3 s^-1

#select dissociation rate coefficient 4 column
kDS4 = data[1:,24] # m^3 s^-1

#select ionization rate coefficient 1 column
kEI1 = data[1:,25] # m^3 s^-1

#select ionization rate coefficient 2 column
kEI2 = data[1:,26] # m^3 s^-1

#select ionization rate coefficient 3 column
kEI3 = data[1:,27] # m^3 s^-1

#select fusion rate coefficient 1 column
kFS1 = data[1:,28] # m^3 s^-1

#select recombination rate coefficient column
kRC = data[1:,29] # m^3 s^-1

#read and store tabulated data using genfromtxt, ignoring first line with strings
data2 = np.genfromtxt("I120-I29-N116-N28.csv",skip_header=1,delimiter=',')

#select time column
time_2 = data2[1:,0] # s

#select D density column
n_D_2 = data2[1:,3] # m^-3

#select D+ density column
n_Dp_2 = data2[1:,4] # m^-3

#select electron density column
n_e_2 = data2[1:,20] # m^-3

##initial calculations
Te = 500
#steady state atomic ratio
R_a = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    #R_a += a_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n
    R_a += a_ratio[n][m] * (8*math.log(10))**m * (math.log(Te))**n

#steady state molecular ratio
R_m = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_m += m_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n

#rate coefficients
i = 0
for ne in n_e:
  if ne <= 1e14:
    #temperature index
    for n in range(0, 9):
      kDS1[i] += coeffsDS1[n][0] * (math.log(Te))**n
      kDS2[i] += coeffsDS2[n][0] * (math.log(Te))**n
      kDS3[i] += coeffsDS3[n][0] * (math.log(Te))**n
      kDS4[i] += coeffsDS4[n][0] * (math.log(Te))**n
      kEI1[i] += coeffsEI1[n][0] * (math.log(Te))**n
      kEI2[i] += coeffsEI2[n][0] * (math.log(Te))**n
      kEI3[i] += coeffsEI3[n][0] * (math.log(Te))**n
      kRC[i] += coeffsRC[n][0] * (math.log(Te))**n
  elif ne >= 1e22:
    for n in range(0, 9):
      #density index
      for m in range(0, 9):
        kDS1[i] += coeffsDS1[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kDS2[i] += coeffsDS2[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kDS3[i] += coeffsDS3[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kDS4[i] += coeffsDS4[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kEI1[i] += coeffsEI1[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kEI2[i] += coeffsEI2[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kEI3[i] += coeffsEI3[n][m] * (8*math.log(10))**m * (math.log(Te))**n
        kRC[i] += coeffsRC[n][m] * (8*math.log(10))**m * (math.log(Te))**n
  else:
    #temperature index
    for n in range(0, 9):
      #density index
      for m in range(0, 9):
        kDS1[i] += coeffsDS1[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kDS2[i] += coeffsDS2[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kDS3[i] += coeffsDS3[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kDS4[i] += coeffsDS4[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kEI1[i] += coeffsEI1[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kEI2[i] += coeffsEI2[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kEI3[i] += coeffsEI3[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n
        kRC[i] += coeffsRC[n][m] * (math.log(ne/1e14))**m * (math.log(Te))**n

  kDS1[i] = 1e-6 * math.exp(kDS1[i])
  kDS2[i] = 1e-6 * math.exp(kDS2[i])
  kDS3[i] = 1e-6 * math.exp(kDS3[i])
  kDS4[i] = 1e-6 * math.exp(kDS4[i])
  kEI1[i] = 1e-6 * math.exp(kEI1[i])
  kEI2[i] = 1e-6 * math.exp(kEI2[i])
  kEI3[i] = 1e-6 * math.exp(kEI3[i])
  kRC[i] = 1e-6 * math.exp(kRC[i])

  RDS1[i] = kDS1[i] * ne * n_D2[i]
  RDS2[i] = kDS2[i] * ne * n_D2[i]
  RDS3[i] = kDS3[i] * ne * n_D2p[i]
  RDS4[i] = kDS4[i] * ne * n_D2p[i]
  REI1[i] = kEI1[i] * ne * n_D[i]
  REI2[i] = kEI2[i] * ne * n_D2[i]
  REI3[i] = kEI3[i] * ne * n_D2p[i]
  RRC[i] = kRC[i] * ne * n_Dp[i]

  SDp[i] = REI1[i] + 2*REI3[i] + RDS2[i] + RDS3[i] - RRC[i] - 2*RFS1[i]
  Sem[i] = REI1[i] + REI2[i] + REI3[i] + RDS2[i] - RDS4[i] - RRC[i]
  SD[i] = -REI1[i] + 2*RDS1[i] + RDS2[i] + RDS3[i] + 2*RDS4[i] + RRC[i]
  SD2p[i] = REI2[i] - REI3[i] - RDS3[i] - RDS4[i]
  SD2[i] = -REI2[i] - RDS1[i] - RDS2[i]




  i += 1



##plotting
#species densities
fig = plt.figure()
plt.title('Species Densities')
plt.axhline(y=(math.exp(R_a))*n_D[-1],color='black',linestyle='--',label='Predicted n${}_{D^+}$')
plt.plot(time, n_D, color='green', label='n${}_D$')
plt.plot(time, n_Dp, color='red', label='n${}_{D^+}$')
plt.plot(time, n_e, color='purple',linestyle='--', label='n${}_e$')
plt.plot(time, n_D2, color='blue', label='n${}_{D_2}$')
plt.plot(time, n_D2p, color='orange', label='n${}_{D_2^+}$')
plt.yscale("log")
plt.ylim(1e7, 1e26)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig = plt.figure()
plt.title('Reaction Rates')
plt.plot(time, RDS1, label='RDS1')
plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3')
plt.plot(time, RDS4, label='RDS4')
plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2')
plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC')
plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_rates.png",dpi=600,bbox_inches='tight')

#reaction rates for molecular ion verification
fig = plt.figure()
plt.title('Reaction Rates')
#plt.plot(time, RDS1, label='RDS1')
#plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3',linestyle='--',color='tab:green')
plt.plot(time, RDS4, label='RDS4',linestyle='--',color='tab:red')
#plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2',color='tab:brown')
plt.plot(time, REI3, label='REI3',linestyle='--',color='tab:pink')
#plt.plot(time, RRC, label='RRC')
#plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_rates_D2p.png",dpi=600,bbox_inches='tight')

#reaction rates for atomic neutral verification
fig = plt.figure()
plt.title('Reaction Rates')
plt.plot(time, RDS1, label='RDS1',color='tab:blue')
plt.plot(time, RDS2, label='RDS2',color='tab:orange')
plt.plot(time, RDS3, label='RDS3',color='tab:green')
plt.plot(time, RDS4, label='RDS4',color='tab:red')
plt.plot(time, REI1, label='REI1',linestyle='--',zorder=6,color='tab:purple')
#plt.plot(time, REI2, label='REI2')
#plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC',color='tab:gray')
#plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_rates_D.png",dpi=600,bbox_inches='tight')

#reaction rate coefficients
fig = plt.figure()
plt.title('Reaction Rate Coefficients')
plt.plot(time, kDS1, label='kDS1')
plt.plot(time, kDS2, label='kDS2')
plt.plot(time, kDS3, label='kDS3')
plt.plot(time, kDS4, label='kDS4')
plt.plot(time, kEI1, label='kEI1')
plt.plot(time, kEI2, label='kEI2')
plt.plot(time, kEI3, label='kEI3')
plt.plot(time, kRC, label='kRC')
plt.plot(time, kFS1, label='kFS1')
plt.yscale("log")
#plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate Coefficient (m${}^{3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_coefficients.png",dpi=600,bbox_inches='tight')

#source terms
fig = plt.figure()
plt.title('Source Terms')
plt.plot(time, SD, color='green', label='S${}_D$')
plt.plot(time, SDp, color='red', label='S${}_{D^+}$')
plt.plot(time, Sem, color='purple',linestyle='--', label='S${}_e$')
plt.plot(time, SD2, color='blue', label='S${}_{D_2}$')
plt.plot(time, SD2p, color='orange', label='S${}_{D_2^+}$')
plt.yscale("symlog")
plt.yticks([-1e24, -1e21, -1e18, -1e15, -1e12, -1e9, -1e6, -1e3, 0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24])
plt.ylim(-1e25, 1e25)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Production Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("working_sources.png",dpi=600,bbox_inches='tight')

###exponential case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I120-I26e12-N116-N213.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select D2 density column
n_D2 = data[1:,1] # m^-3

#select D2+ density column
n_D2p = data[1:,2] # m^-3

#select D density column
n_D = data[1:,3] # m^-3

#select D+ density column
n_Dp = data[1:,4] # m^-3

#select electron density column
n_e = data[1:,20] # m^-3

#select dissociation rate 1 column
RDS1 = data[1:,5] # m^-3 s^-1

#select dissociation rate 2 column
RDS2 = data[1:,6] # m^-3 s^-1

#select dissociation rate 3 column
RDS3 = data[1:,7] # m^-3 s^-1

#select dissociation rate 4 column
RDS4 = data[1:,8] # m^-3 s^-1

#select ionization rate 1 column
REI1 = data[1:,9] # m^-3 s^-1

#select ionization rate 2 column
REI2 = data[1:,10] # m^-3 s^-1

#select ionization rate 3 column
REI3 = data[1:,11] # m^-3 s^-1

#select fusion rate 1 column
RFS1 = data[1:,12] # m^-3 s^-1

#select recombination rate column
RRC = data[1:,13] # m^-3 s^-1

#select D source column
SD = data[1:,14] # m^-3 s^-1

#select D2 source column
SD2 = data[1:,15] # m^-3 s^-1

#select D2+ source column
SD2p = data[1:,16] # m^-3 s^-1

#select D+ source column
SDp = data[1:,17] # m^-3 s^-1

#select electron source column
Sem = data[1:,18] # m^-3 s^-1

#select T+ density column
n_Tp = data[1:,19] #m^-3 s^-1

#select dissociation rate coefficient 1 column
kDS1 = data[1:,21] # m^3 s^-1

#select dissociation rate coefficient 2 column
kDS2 = data[1:,22] # m^3 s^-1

#select dissociation rate coefficient 3 column
kDS3 = data[1:,23] # m^3 s^-1

#select dissociation rate coefficient 4 column
kDS4 = data[1:,24] # m^3 s^-1

#select ionization rate coefficient 1 column
kEI1 = data[1:,25] # m^3 s^-1

#select ionization rate coefficient 2 column
kEI2 = data[1:,26] # m^3 s^-1

#select ionization rate coefficient 3 column
kEI3 = data[1:,27] # m^3 s^-1

#select fusion rate coefficient 1 column
kFS1 = data[1:,28] # m^3 s^-1

#select recombination rate coefficient column
kRC = data[1:,29] # m^3 s^-1

##initial calculations
#steady state atomic ratio
R_a = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_a += a_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n

#steady state molecular ratio
R_m = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_m += m_ratio[n][m] * (math.log(n_e[-1]))**m * (math.log(T_e))**n

##plotting
#species densities
fig = plt.figure()
plt.title('Species Densities')
plt.plot(time, n_D, color='green', label='n${}_D$')
plt.plot(time, n_Dp, color='red', label='n${}_{D^+}$')
plt.plot(time, n_e, color='purple',linestyle='--', label='n${}_e$')
plt.plot(time, n_D2, color='blue', label='n${}_{D_2}$')
plt.plot(time, n_D2p, color='orange', label='n${}_{D_2^+}$')
plt.yscale("log")
plt.ylim(1e7, 1e26)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("exponential_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig = plt.figure()
plt.title('Reaction Rates')
plt.plot(time, RDS1, label='RDS1')
plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3')
plt.plot(time, RDS4, label='RDS4')
plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2')
plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC')
plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("exponential_rates.png",dpi=600,bbox_inches='tight')

#reaction rate coefficients
fig = plt.figure()
plt.title('Reaction Rate Coefficients')
plt.plot(time, kDS1, label='kDS1')
plt.plot(time, kDS2, label='kDS2')
plt.plot(time, kDS3, label='kDS3')
plt.plot(time, kDS4, label='kDS4')
plt.plot(time, kEI1, label='kEI1')
plt.plot(time, kEI2, label='kEI2')
plt.plot(time, kEI3, label='kEI3')
plt.plot(time, kRC, label='kRC')
plt.plot(time, kFS1, label='kFS1')
plt.yscale("log")
#plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate Coefficient (m${}^{3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("exponential_coefficients.png",dpi=600,bbox_inches='tight')


#source terms
fig = plt.figure()
plt.title('Source Terms')
plt.plot(time, SD, color='green', label='S${}_D$')
plt.plot(time, SDp, color='red', label='S${}_{D^+}$')
plt.plot(time, Sem, color='purple',linestyle='--', label='S${}_e$')
plt.plot(time, SD2, color='blue', label='S${}_{D_2}$')
plt.plot(time, SD2p, color='orange', label='S${}_{D_2^+}$')
plt.yscale("symlog")
plt.yticks([-1e24, -1e21, -1e18, -1e15, -1e12, -1e9, -1e6, -1e3, 0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24])
plt.ylim(-1e25, 1e25)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Production Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("exponential_sources.png",dpi=600,bbox_inches='tight')
