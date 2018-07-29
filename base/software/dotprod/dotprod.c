#include <stdio.h>
#include "sys/alt_timestamp.h"
#include "sys/alt_cache.h"
#include "system.h"
#include "nios2.h"

#define HAL_PLATFORM_RESET() NIOS2_WRITE_STATUS(0); NIOS2_WRITE_IENABLE(0); ((void (*) (void)) NIOS2_RESET_ADDR) ()



int dot_product(int *, int *, size_t);

int main(void)
{
        int a[1100] = {-132525097, -29263687, -114528767, 81819284, 61401591, 12467458, 141567353, 24751787, 5021798, 74349591, -128241185, -107765271, 38910598, -14453669, -52644777, -140920520, -113777557, 83965156, 57313600, 50823415, -62129044, 68900724, -68055099, 128952411, -141264957, -40618966, 87825125, 21059575, -87058716, -86471596, -71569016, 107366638, 55643320, -130475391, 71189140, 131161848, 134536342, 79875741, -14699998, -57301612, -73660681, -12628403, -88821458, 85645293, -58786378, -58202006, -24044228, 31912438, -16032943, -40900067, -24099722, 40903842, 55674534, -51927466, -28356077, 9976210, -47602993, 136387461, 139636538, -34625634, 8042393, 77413541, -118605718, -15341085, -37558613, 32039652, -39508338, -73552403, -3258126, 30950994, -116261084, 123845613, 55186520, -123296076, -121302079, 16031815, -143649573, -99398352, -66566354, 124820946, 146867410, 76468323, -93519858, -23568465, -24762382, 113123776, 66360358, -131698955, 7286053, -133800043, 134082767, 74547306, 8870182, 12086043, -28168319, -60214727, -34626115, 104952934, 14397084, -48566039, 98271361, 87160915, -144006214, -124817001, 56546528, -37474581, 37699795, -4397374, 108483590, 6874461, 134442270, -5236161, -13810818, -80844571, -87779775, -114496578, -105309800, -94085745, 69806954, -83247924, 48933243, -30458588, 98288584, 89987818, 83933965, -10533576, -142240682, -6773090, 43000935, 117887388, 63191878, -111563642, -17200582, -98617430, -120286238, -128661939, 76012083, 114864369, 102998609, 71607424, 99220584, 13964566, 141752452, 61621371, 145476281, -136146498, -31497283, -15429393, -98630686, 136888452, 8287957, -91889279, -69431076, -10670332, -144266008, 47415527, -98222637, 110715999, 120524198, -108862784, 119440614, 82000902, -89777701, 75889534, -50086940, 2685985, 57559607, 131115927, -58085098, 21488779, -110623449, 39303180, -79497067, -51323428, 29448062, 96276757, 114110324, -98050916, 22946545, -98873635, -75657435, 102127369, -41155268, -64442163, -1489223, 85123139, -2835260, 130817551, -134726708, 96042044, -77851114, 76555929, 48509515, -52985045, 114803411, -26357909, 64559280, 22287465, 82846985, -113760604, 62408479, 34633442, -133814228, -109101809, 21565732, -74732165, 30293065, -22768652, -104480152, -85738236, 20234536, -22928810, 138334047, -65817337, -108803655, -121769470, 56766736, 146985639, 110798268, 122903567, 128895466, -37071899, -98130611, -95100682, 116380774, -41411436, -125044117, 125696424, -106355073, -119944041, 104926880, 10443931, -141081605, -21079934, -61801534, 49910788, -122600922, -118512627, 6842474, -54975296, -68020447, 80552002, 51589354, 118707103, 48877249, -121107902, -114452698, -143864734, 100269035, 34327783, 20261121, -25652327, -102166881, -58021107, -37716692, 80371564, 76903439, 130117471, 17338608, -30322030, 132645261, -42589028, 27373511, -37147101, 11889360, 119039064, 6738256, 128560923, 144320212, -24591260, 74015838, 3500819, -4590778, 22111681, 2452626, 96185722, 14162069, -135966563, -18286959, -73540355, 132487220, 52835557, 88042862, 124067805, -18534325, 3744970, -126225798, -28447877, 108301113, -98237014, -27671863, -118243297, -117655910, -2410401, 100765183, -65852286, 93153567, 9432, -94061982, 15953569, -36990403, 127895054, -144404880, 20278740, -127643008, -1323763, 14366196, -98887210, 127110078, 17682111, -48024994, -123816903, 124476242, 130239488, -6194233, -61285420, -52500124, -60764639, 85775505, -93331727, 32604964, 33243758, 82762945, 55404922, -98323341, -46994770, -114760285, -70455598, 72777633, 2880991, 123131902, 42868778, -26830317, 50563763, -857015, 139581502, 133131749, 8698310, 41712487, -94925595, -24751425, -43792978, -145364599, 67909982, 73581510, 58676594, -105356855, 74568823, 83576131, -114153339, 81172779, -4084718, -24837071, -77982217, -85659747, 6454888, -133687773, 9576708, -61859968, 145679137, -59367247, -64456595, -142568942, -99568236, 54361652, 110245273, -25504586, 131394466, -3309841, -14217187, -3722384, 103267034, -44230337, -51259187, -140756056, 147265367, 69070921, -1538912, 115799013, -108679642, 91385563, -6390498, 90108258, 32060201, 81621282, -34851287, -53419126, 51117036, 69962765, 36698005, -13566326, -23983638, 43725994, 74222602, 126190, -11193862, -71166048, 27874002, 64679437, 63723893, 60893898, -67477994, -61579918, 121522207, -70713603, 99534718, 9551006, -3889105, 20645526, 107237438, 86479572, -85826824, 32705066, 142746635, 122869186, 135514868, -145892134, -68812235, -78254828, -125964205, -139012277, -112201163, 23912731, 133893959, 53604486, 40690789, 22509422, 140535049, -104815561, 68773898, -51505446, 95240674, -76689306, 43120276, -90081381, 65712949, 123797570, -93678096, -81375090, 48520658, -10720712, -94216973, 41104508, 129810750, -125968287, -101027827, 44020527, -1454269, 108181782, -24941343, 92020430, -87954916, 136962477, 116347011, -18556702, 23746134, 108591787, -66212962, -74010362, -147273474, -97979591, -9798601, -28426381, 117422500, -68641104, 51502649, 37136696, 36896771, -119693979, -7415041, -4681140, -52391438, 7066322, -138392482, -99709787, 36995911, 8614015, -54948385, -96860574, 130565175, 101245739, 61040663, 109741667, 45002253, -47552318, -89139844, 29782442, -107033564, 28897451, 127100103, 141094784, 143428966, -113865781, 130930804, -97459432, -3739931, -80874212, 97566841, -47997619, -53594884, -15754584, 134878402, -88245238, 62559060, 23700417, -4449332, 90766307, -44860959, -41909255, 132528646, 136648610, 138896446, 118287230, 146878096, 99086493, -57704331, 134979798, -3370964, -46855322, -758864, 51953251, 147290055, 52182152, -46071041, 134869100, 16380104, -71658760, -25386069, -131816753, 93134311, 52200886, 128003071, -126414181, -112698721, 117327596, 121972974, -58499907, -29955398, -29781214, 56737119, 62729557, 1120364, 39668166, -132400191, -24318670, 79223813, 90889898, -1068262, -136378286, 20555114, -120950117, -85171494, 136855001, -94326100, 43620214, 127442607, -134529759, 63897414, -118981784, -58810843, 69568164, 60525636, 94048156, 59788239, 132326610, 121353048, -11000020, -120698736, -119935348, 135724821, -125296128, -21990196, 107939733, -79472046, 118152510, -23229237, 32011327, -90947243, 106674163, 56418381, 26934035, -56028369, -21082714, 57539265, -136637748, 3175135, 34770852, -63885798, 127448240, 17631364, 105504227, -64346216, -923762, 29893479, 6886890, -97842706, 112328991, -73691188, 69263105, 85624674, -33945207, -146041842, 24981017, -2216613, -98624572, -19640689, -112489123, -19269630, -83295014, -112435684, -110284185, 141600302, 50663994, -85715168, -9126131, 95543604, -496968, -99247226, -62137668, 124337641, 8031932, 130105516, 57786269, 27445899, -25774628, 75622691, 132926601, 142636901, 92364742, -222098, 130759778, 114815181, -69717502, 58033263, -62411312, -138139910, -129746362, 36871699, 6625448, 125955208, -54457901, 82781003, 146765683, -50438290, -97671207, -134790792, 85317797, 81982676, -134087291, 145171449, -133271409, -31537093, 12627956, -93962825, -56982149, -38421308, -52895856, 37426720, 133347010, -58001200, -18232008, 127164711, -9001430, -94571278, -90736906, 126295456, -50625745, -79546893, -36343975, 139462776, 3681311, -141363655, 19926672, 89963877, 5277773, -117100863, 139986319, 130319232, 61768392, 89145056, 46484223, 8035602, 120454909, 12475209, -127290451, -56690309, 48320527, 75619869, -121549618, -83743170, -98027309, -15896699, -85670875, 33706531, 59630646, 79451283, -42937744, 96234125, -80367947, 26796655, -89980448, 89022194, 44959295, 37122915, 29150491, 84354087, -147024515, -17651063, 19374018, 134099297, 80392301, -51914901, -2052000, -120952809, -120510780, -97041513, 51013275, 84483892, -116452030, -138250586, 97455996, -18080594, 115966699, -30010520, -98494208, -144513348, -136154347, -91096212, -79862209, 37123826, -135767248, 118849098, 13229456, 8287175, -43749250, 8477074, -55995465, 100726618, 85228601, 4775136, 71309790, 65065043, -89239605, -130393697, 32290203, 108678662, 136248653, -70268110, -50591199, 40771943, -61040455, 3865060, -90954837, -61176487, -102233971, -108287551, 38806246, -38499668, -133745433, -124704767, 34536733, 92708844, 77466903, -78885841, 146667597, 20218311, -68681044, -17116722, -37944421, -113522171, -60299096, -104616767, -44262618, 3687662, -84673072, -139882043, -123037501, -93599496, 6480892, 107033478, 35146392, 20524795, 80367711, 125997289, -21100762, -126082289, 45991230, 51286114, -125325468, 11859076, -9700077, 42201682, -85250877, 24984289, 39500854, -42808774, 18351237, 92018638, 14585719, -88622912, -36711376, -104305946, 29269524, -19934222, -113916742, 35602917, -115570106, 114815708, -67488866, 58491505, 3245248, 74759287, 34840070, 40942766, -125831584, -50354017, -133998864, -73333702, 30112679, -17522447, -42429359, 33620555, -44084302, 80402448, 41436182, -87050883, 12183990, 91539119, 58328908, -99906798, 130752757, -106552845, 131628628, -71522954, -20944780, -61014808, -66565988, -47392058, -100351189, 139005464, -129669069, 52942902, 24151398, -60946521, -57262694, -96091482, 9809844, 85105475, 59581089, -31158435, 9397913, -1429464, 63883817, 90655615, -98974843, 1257391, 99651094, 75709739, 95215310, -25640303, -70029504, 69075264, -22818624, -62945817, -122228668, 94157606, 84851116, -22211690, 20527944, 80472391, -123085918, 39755188, 59788052, 97169474, -250957, -114802986, 44399201, 130069508, 14411089, 111390542, 128171134, -103004943, -99202466, -48212717, 50881286, 128086343, 116761073, 68415853, -36086932, -134035281, -68982996, 31323415, 139535329, 28294729, -10696329, 85489930, 20872535, -17212710, 111888034, -20888757, 60468926, 27197257, -45157913, 120357883, -82106058, 77387330, 39691695, -6242880, 83685052, 84268992, 47623914, -60349783, -26139566, 139365910, 140071757, -104066292, 60341130, -99228199, 141164247, -57509060, 26448816, 73386940, -131262613, -114888640, -142574704, -12076023, -20326229, 107412236, -146950386, 68459544, -19118665, 75701559, 111917842, -103772884, -67181477, -11742302, 21557933, 133305142, -91876272, -7575427, -90296961, 22261526, 57391940, -19964728, -77099147, 48198125, -63260432, 107942754, 116015723, -77426378, 49797413, -19644840, -70893300, -37081181, 110990681, 56862029, -54258433, 1662744, 83098560, -88444483, 547722, -132561770, 131603613, 20398362, -96977401, 87379884, -43585854, -117066030, 1608604, -126165531, 32377692, -70643777, -35511719, 102729835, 107177557, -11399091, -51199266, -37949032, -112379656, -3518568, -14133425, 34338692, -28875982, -119496422, -100431328, -73254634, -32896482, 62692399, 145867074, 3843373, 76300337, -20637449, 125018145, 143116922, -65407981, -110932543, 128700618, 127418313, 116218761, 17867523, -28204911, 49129104, 132566751, -92341713, 53141861, -69566882, -134078139, -20848866, 73373038, 136390387, 31612422, -115116220, 142882447, 51662948, 41057057, -71304918, 15227264, -106314651, -121335262, 133948053, 86759158, -43135161, 62433783, -28003694, 129182605, 140492811, -121062224, 11274691, -132623134, -22254417, -143800783, -117828214, -16559499, -15598695, -43587944, -32458264, -27494383, -105027654, 67640590, 114083243, 8530094, -114941027, -101277592, 30871903, -9051947, -5475607, -51512970, 18322759, -30670509, 19118581, 117086447, 84857155, 20180106, 101812347, -121487852, 139534214, -78364564, -18470895, -65320133, -123000928, -147344478, -9815073, 77450324, -12130597, 131722715, 112246713, 139342990, -51105331, -26063243, -77507120, 106579426, -31531877, 137276783, 119932784, -55660931, -137480345, 76298226, -65085420, -143139039, -120558415, -59890505, 99333204, -84236691, 63665679, 57347895, -110185733, -45468896, -19217945, 53677340, -140053333, 145165073, -79902095, -88640353, -22705398, 84329293, 112702365, 4003213, 82427010, -91659936, -139888357};
        int b[1100] = {-91544439, 62317874, -42997548, 4955426, -116740977, -137129011, -76613313, -31680432, -18028760, -63204082, -41745355, 115477823, -116338843, 47778751, -29520721, 143586495, -34896852, -110526985, 106737394, 15681747, 36957794, 10260181, -7894351, -92135236, -91951234, -106971035, 30568694, -84462545, -4122120, -120723977, 147098036, 95538556, 127486495, 46452550, -89543300, 12529923, -36168944, -6864506, -35169129, -155909, -4961517, -66558284, -83261528, -103069447, 120188432, -90523534, 143164220, -23730120, 122002613, -81947633, -114681220, 71012413, -82646602, 66842381, -7505502, -110676292, -24346054, 60938626, 87549386, -104785612, 97097098, 6416383, 35994348, 35058147, -82322304, 133871403, -90444800, 86400830, 42775885, 62705500, 53617371, 113035866, -16839970, 56444633, -82083803, 110112105, 79654790, -137344924, -58184359, -76521134, 76149174, -2981882, -66112056, -56009624, 782406, -96722450, -101020789, 38519952, 54694537, -56666579, 119631698, -58001141, -48794046, -848754, -89887624, -132006350, 80762150, -43987096, -135431982, -102312684, 45136909, -88525675, -106512126, 2618550, -42287515, -26209463, 117611554, 12937683, -7480294, 105716222, 111478650, 52325971, 71812276, 124899293, 20508748, -127937260, -117042361, -18128944, -123213872, 13050629, 65564917, -24316006, 29226168, 104036935, -126368699, -43423061, -2992996, -56192198, -40806020, 14202512, -55711821, -93234573, -137312852, -68543979, -136704315, -75669951, -14434576, 143515462, 115964469, 44022731, -85337435, -104992731, 96465148, -46513778, -81308573, 132793348, 91560654, 113870620, -125069250, 145895556, -26179399, -20572767, -115205295, 141223658, -58900240, 134960623, 96780552, -128388648, 57479288, 145651488, -50413259, 128325584, 12673497, -34260000, 55809793, -35602709, -4000246, 123003680, -31800441, -146483553, -18942715, -39943139, -127980823, 1839978, -11495189, 60659743, 5385287, -131016026, 27207689, -115582390, 6648434, -142962789, -134550994, -72160283, 99582622, 63023603, 5806930, 142779850, -30024812, -57920701, -118401598, 89955746, -119846611, -76657580, 104149670, 89791422, -24370770, 32819559, -54456133, -130731130, 18238747, -101687095, 2565068, 56112365, 39743671, -47686722, 141314775, 37119956, -33873409, 20141782, -89843143, -59510206, 104214414, 103779292, 2756961, -105093538, 112396658, 73040907, -117643433, 120293538, 109777702, -123488891, -46460997, -56886777, -73260457, 119630713, -20533623, 102573383, -124442771, -28526945, -125464662, 121076624, -120321595, -37952740, 106293131, -91880037, -23793718, -10563827, -122220267, -45726318, -122595467, -30782938, -76264068, -66278379, -81850889, -120426968, 25578935, -44750937, 78910406, 136535211, -58954814, 34223907, -145045345, 141653547, 146458571, -104230372, -79610283, -77955839, -96493871, 126134701, 41206718, -54004852, -66990891, 131870964, 1294839, 83411254, -21968922, -87316351, -15634603, -14596916, -122631879, -116163149, 46432291, -28721267, -60696345, -29608994, 123416015, 92741380, 49206948, 38743683, -66642924, 21872472, -146281036, 7142041, -87431105, -3429074, 103543865, -89447476, 107683262, 131779595, 127046874, -68747883, -14808460, 93462561, 117444708, 143044438, -32897632, -110571564, -49073208, -100871744, -128199956, 135859838, -114312665, 129469754, 86500810, 58801307, -68984003, 28940560, -71818861, 26729699, 31888293, -88028204, 67622278, 40926283, -35536583, -111996243, 95114022, 80035827, -93389424, 46649185, -113857314, -21893622, -68139416, -126870431, 18026956, -79273660, 11488519, 61885262, -43680026, 117916835, 110126615, -78507282, 122779820, 31959307, 127753443, -95835542, -141300207, -133185294, -75186371, 35643430, -75250828, 49238751, 113425120, -63748698, -108498459, 88814082, -2612477, -55829306, -17420825, -115713151, 30901869, 55220908, -743596, -126701886, -58693542, -101686122, 52350366, -41960111, 70711489, -90047216, 66999936, -132239478, 119630163, 102298357, 96534709, 115865799, 28551848, -91867718, -34021091, -63455038, -13252548, -112442810, -92937346, -100621639, -17909066, -135722926, 32375360, -18813102, 44595464, 24326047, -67271310, -11994482, 2529929, -72704896, -76975136, -33751058, 108193516, 99198213, -67673626, 124494048, 79233943, -38583536, -3209595, 66704460, -79759479, -46834008, 97484642, 51733833, 26539080, 122025000, -63888519, -139792069, -27288194, -72672547, 2486134, -27072991, 119753569, 130939333, 70368146, 83468042, -47263999, -146143443, 92560800, -127175621, -88249071, 15219373, 105249472, 26319294, 71539400, 23352426, 9421327, -89757314, 118564628, 59411974, -34854478, -99021104, 105595065, -135562904, -54652154, 52383216, -76761285, 32293231, -130541893, -124547465, 82266256, 50723283, -115303947, 118961574, 17066053, -34646985, -121318774, 50837862, 97964269, -78376690, -101141482, -29638447, 140397566, 43318959, -126171578, 147205333, -72180839, 34570352, -103093553, -22466258, -90823657, -101213448, -88530934, -145590919, 78581534, -75848045, -15772136, -68348915, 122149552, 126789656, -88632480, 89923202, 80153349, -76522474, -143800844, -59926387, 40794472, -71939204, 120522397, -61637671, -833736, 16950653, -111614799, -55330754, 93873660, -138095885, 97390742, 46260377, -72317272, -46751036, 97245266, -79739329, -92751114, 88466270, -98210965, 45110028, 93531018, -117240551, 86581668, 133896595, 73537340, -45148927, 47637529, 50571673, 66547831, 73774684, -90302434, 120667622, -143115687, -113460397, -108528349, -91744786, 27483775, -138563440, 50492705, 120988953, -89429450, -10418583, -116872123, -87554103, 78234462, 59013407, -23068141, 125333979, -77061174, -133610975, 101455988, -37288420, -107496930, -128297099, 78727452, 115325642, 72182885, 45049857, 79909130, -86580165, 24340395, -19563797, 94579475, -109673618, -30239194, -108650904, -43501645, 88004774, -23126339, -69581475, -8332993, 55121312, 121695162, -95226863, 12984359, 90032949, -63565922, 105562965, 141060608, -5578902, -77683646, -136555287, -33306799, 88163584, 109105942, -11320815, 101827116, -25727780, -127963575, 69122280, 130949726, -6896915, 27382919, 62514931, -103578811, -95145106, 14282587, 99755219, -99653809, -134901824, -1167400, 18462499, -61625848, 94477095, 121332534, -86585052, 84566219, 73997129, -31164364, 48175146, -136269912, 83989833, -48058435, 37533222, -55269872, 29714974, -42848888, -127104032, 77172476, -21229404, 130088657, -96815410, -135066167, -111345335, -36456896, 16432820, 108714007, 70259614, 126389099, 34542183, 76083625, -103808752, 1543435, -50508058, 117631345, 116471738, -63531151, 129306867, -41763401, -103166893, -126194353, -122830431, -56096536, 132957578, -93333451, -97531629, 11603594, -117834201, -47662205, -14893653, -116358809, -29738632, -135686598, 135230942, 3263576, 76489099, 93504166, -50600931, 129153522, -54809170, 105617139, 65300541, 60109430, 56259841, -25594692, 78845836, -102410153, 62344786, 128267088, -81918089, -66649942, 83170386, 96323963, -55502921, 104016842, -79765751, -72256482, -98780830, -121913947, 100530850, 98796681, 7024953, 10070098, -12278494, 78280657, 32734379, -118101045, 109796173, -141390808, 134614296, 65984669, -124172594, -92091937, -11141847, 96584275, -72642246, 144135195, -67614756, -12454330, -25755005, 51708275, -46497364, 102084418, -122788008, -44803172, 38079625, 115869140, 135982863, 65708487, 52283195, -130151227, 34196907, -141495354, -1013296, 125083729, -89484501, -17187944, -11951870, -11747418, 88816273, 126283167, 62199882, 17082723, 114288037, 90172810, -136245776, -81828941, 12445560, 31386044, -1520962, -112309465, 135469950, 103051801, 133094482, -115461737, -4537188, -53120372, 90214176, 17555203, 90748481, -113095210, 79387387, 76270734, 11461699, -141815168, -53670543, -111890473, -71230883, 130240157, 323796, -124060566, -9302042, 48871083, -114318297, 53019210, -98575911, 68485995, 74719821, 30236437, 97940380, -59743327, 23134899, -21438218, 142628983, -70628089, 93299062, 56558072, -65478158, 99843508, -81541006, -47627844, 16179507, 101628999, -33976704, 16376304, 125501749, 46398198, 23617655, -106060945, 100873234, -24886762, -10137182, 103965318, -71386370, 97536541, 102240736, -51251806, 37587699, 112180208, -108958874, -7683360, 1387536, -90968976, 55258449, 102258784, 73112302, 15932003, 134554859, -130206282, 32767769, 2615560, -141586869, -44885108, -42113386, 87385667, -84771693, 53008572, 83944711, 27013947, -130011914, -71338609, -100212700, 114200404, 89641911, -122593518, 145461670, 84887169, 140537035, -44953537, 134237039, -58664548, 12060100, -20855938, -35407739, 6365736, -3150672, -88346726, 74661689, 143964287, -109025012, 115563736, 129200562, -32401072, 77123235, -68047056, 809478, -104117247, -20397501, 100895989, 68108654, 86497918, 30121367, 114670314, -124711553, 91660439, 112394558, -127721424, -127703808, 138788322, 105426012, 90026952, 70544891, -55794176, -95638747, 31278752, 42863474, -17001704, -55096982, -86165658, -66085461, 6994246, -12918718, -145301090, -66424001, -128851232, -115480389, 100814180, -27221196, -36286342, 98881059, -11994927, -5092127, -8642173, 86915336, -78841340, -84021189, 53591110, -7115736, -60315103, 103691998, -94888427, -147022938, 5279391, 113001252, 136979717, -3992140, -118489157, 38586511, -124925918, -5477598, -45487075, -119918153, 43497902, 140380453, -21792435, 20613955, 81721738, 89232194, -48547948, -85286427, 107383046, -41491992, -117850561, 17475485, -58566197, -95042943, -33872514, 22824341, 74611604, -16995045, 16060656, -88969390, -21183044, -138776299, 115759974, -63519469, -110052808, -138176725, 120772099, -46317666, -102401321, -87180401, 115933179, -72475183, 84211747, 125500944, -28139533, -8518416, 112404734, -128588024, 22599923, -84718995, -41632432, 13688561, -90810664, 57352029, -13612198, 36816298, 55764526, 5738321, -54245911, 146886679, 117399808, -44158118, 39012115, 89260873, -39314933, -144033398, -61254357, 33998313, -40201890, 81514157, -62364892, 93382980, 104111333, 137944935, 129924185, -138913140, 90916505, 95353710, -50018639, 107015912, -107737406, 131383320, -140111315, 110708551, 113839800, 90615754, -61760540, 70241679, -63143218, 98279334, -91443867, -77836284, 36378560, -97230457, 67079546, 20529536, 108582677, 12950102, -9689048, -85397776, -96266315, -88671129, -111038411, -137694575, -88487097, 48315141, 59388330, 50350603, -138161000, -122400408, -5789578, 111478224, 1700481, -82703274, -67487558, 101293061, 102583708, -91569018, -118223378, -113171855, -62129645, -52547069, 2624479, 83073647, 77192447, -141151869, 133755801, 146411477, 39588779, -98710673, -124199476, -62552076, 94841757, 15596837, -121015373, -49952798, -86476420, 132984421, -66969674, 79228112, 24233182, -67224409, 102502574, 113979525, 113606271, -71786952, -4741221, -26190116, -145579082, 16989475, -69588519, -116743335, 32073656, 92665662, -134880469, 41333233, 101388403, -118014619, 70326408, -8051439, 133382726, -48735893, 101355438, 88209571, 146812026, 97477372, 48610082, 48829949, -110359788, 117145568, -4595116, 140676468, -53585570, 108429909, -35150686, 127016940, -93338123, 24904372, 98134776, -143875294, -32298529, 50938937, 40430050, -20621813, -113784989, -121318326, -98756918, 125785696, 121161828, 68248874, -20679222, -60750483, -69922928, 121579985, 80174505, 129858575, 78681023, 28554512, -93196737, 146399841, 21945724, -115318232, -104275705, 140925689, -72161085, 51752370, -79756033, -57353313, 49523962, 65945067, 79404587, -144077237, 8824434, 143577596, 39684301, -20933732, -65727834, -66296177, -127188108, -102158310, 57872092, 20381527, -33034059, 87594484, 51152501, 137427786, 80171721, 80683206, -103835314, -6121829, -23558305, 92331693, -52152645, -136869999, 130201615, -97902313, 37305698, -27128299, 4726730, -102234650, -20339566, -43019525, 100121334, 117602590, 94446566, -99979541, -126304097, -73866916};

          if (alt_timestamp_start() < 0)
            {
              printf ("No timestamp device is available.\n");
            }

        alt_icache_flush_all();
        alt_dcache_flush_all();

        int x;
        alt_u32 checksum_start_time = alt_timestamp();


        x = dot_product(a, b, sizeof(a) / sizeof(a[0]));

        alt_u32 checksum_end_time = alt_timestamp();
        alt_u32 i = checksum_end_time - checksum_start_time;

        printf("%ld\n", i);


        HAL_PLATFORM_RESET();
}

int dot_product(int *a, int *b, size_t n)
{
        int sum = 0;
        size_t i;

        for (i = 0; i < n; i++) {
                sum += a[i] * b[i];
        }

        return sum;
}