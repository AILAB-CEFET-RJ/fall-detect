====================================================================
===========================MobiActDataset===========================
The NEW version of the MobiAct dataset includes:
 •	Four different types of falls performed by 66 participants
 •	Eleven different types of ADLs performed by 19 participants and nine types of ADLs performed by 59 participants (plus one activity "LYI" which results from the inactivity period after a fall by 66 participants)
 •	Five sub-scenarios which construct one scenario of daily living, which consists of a sequence of 50 activities and performed by 19 participants.

The new released version of the MobiAct dataset includes:
 • The raw recorded data in txt format, separated by each activity
 • The annotated data in csv format, separated by each activity


Filename format:
<ADL OR FALL OR SCENARIO_CODE>_<SENSOR_CODE>_<SUBJECT_ID>_<TRIAL_NO>.txt

examples:
1 -->	WAL_acc_5_1.txt
2 -->	STD_ori_9_5.txt
3 -->	FKL_gyro_3_2.txt
4 -->	SRH_acc_1_1.txt


Subjects:
+------+---------+-----------+-------+----------+----------+----------+
|  ID  |  Name   |  Surname  |  Age  |  Height  |  Weight  |  Gender  |
+------+---------+-----------+-------+----------+----------+----------+
|    1 | sub1    | sub1      |    32 |      180 |       85 |  M       |   
|    2 | sub2    | sub2      |    26 |      169 |       64 |  M       |
|    3 | sub3    | sub3      |    26 |      164 |       55 |  F       |  
|    4 | sub4    | sub4      |    32 |      186 |       93 |  M       |   
|    5 | sub5    | sub5      |    36 |      160 |       50 |  F       |    
|    6 | sub6    | sub6      |    22 |      172 |       62 |  F       |    
|    7 | sub7    | sub7      |    25 |      189 |       80 |  M       |   
|    8 | sub8    | sub8      |    22 |      183 |       93 |  M       |    
|    9 | sub9    | sub9      |    30 |      177 |      102 |  M       |   
|   10 | sub10   | sub10     |    26 |      170 |       90 |  F       |  
|   11 | sub11   | sub11     |    26 |      168 |       80 |  F       |  
|   12 | sub12   | sub12     |    29 |      178 |       83 |  M       |   
|   13 | sub13   | sub13     |    24 |      177 |       62 |  M       | 
|   14 | sub14   | sub14     |    24 |      178 |       85 |  M       |   
|   15 | sub15   | sub15     |    25 |      173 |       82 |  M       | 
|   16 | sub16   | sub16     |    27 |      172 |       56 |  F       |   
|   17 | sub17   | sub17     |    25 |      173 |       67 |  M       |   
|   18 | sub18   | sub18     |    25 |      176 |       73 |  M       |   
|   19 | sub19   | sub19     |    25 |      161 |       63 |  F       |   
|   20 | sub20   | sub20     |    26 |      178 |       71 |  M       |   
|   21 | sub21   | sub21     |    25 |      180 |       70 |  M       |   
|   22 | sub22   | sub22     |    22 |      187 |       90 |  M       |   
|   23 | sub23   | sub23     |    23 |      171 |       64 |  M       |   
|   24 | sub24   | sub24     |    21 |      193 |      112 |  M       |   
|   25 | sub25   | sub25     |    22 |      170 |       62 |  F       |    
|   26 | sub26   | sub26     |    25 |      163 |       60 |  F       |   
|   27 | sub27   | sub27     |    25 |      180 |       82 |  M       |  
|   28 | sub28   | sub28     |    23 |      178 |       70 |  Ì       |   
|   29 | sub29   | sub29     |    27 |      186 |      103 |  M       |    
|   30 | sub30   | sub30     |    47 |      172 |       90 |  M       |   
|   31 | sub31   | sub31     |    27 |      170 |       75 |  M       |   
|   32 | sub32   | sub32     |    25 |      190 |       77 |  M       |   
|   33 | sub33   | sub33     |    27 |      171 |       70 |  M       |   
|   34 | sub34   | sub34     |    24 |      175 |       85 |  Ì       |    
|   35 | sub35   | sub35     |    23 |      181 |       76 |  M       |    
|   36 | sub36   | sub36     |    22 |      164 |       62 |  F       |   
|   37 | sub37   | sub37     |    25 |      172 |       63 |  M       |  
|   38 | sub38   | sub38     |    21 |      170 |       88 |  F       |    
|   39 | sub39   | sub39     |    26 |      174 |       79 |  M       |    
|   40 | sub40   | sub40     |    23 |      178 |       95 |  M       |    
|   41 | sub41   | sub41     |    20 |      172 |       67 |  F       |  
|   42 | sub42   | sub42     |    22 |      173 |       73 |  M       |   
|   43 | sub43   | sub43     |    24 |      179 |       80 |  M       |   
|   44 | sub44   | sub44     |    25 |      176 |       80 |  M       |  
|   45 | sub45   | sub45     |    26 |      175 |       92 |  M       |   
|   46 | sub46   | sub46     |    23 |      175 |       68 |  F       |   
|   47 | sub47   | sub47     |    21 |      180 |       85 |  M       |  
|   48 | sub48   | sub48     |    22 |      180 |       80 |  M       |   
|   49 | sub49   | sub49     |    23 |      178 |       75 |  M       |    
|   50 | sub50   | sub50     |    23 |      165 |       50 |  F       |   
|   51 | sub51   | sub51     |    23 |      171 |       70 |  M       |    
|   52 | sub52   | sub52     |    20 |      179 |       79 |  M       |  
|   53 | sub53   | sub53     |    27 |      186 |      120 |  M       |   
|   54 | sub54   | sub54     |    27 |      164 |       55 |  F       |    
|   55 | sub55   | sub55     |    28 |      178 |       78 |  M       |    
|   56 | sub56   | sub56     |    29 |      170 |       75 |  M       |  
|   57 | sub57   | sub57     |    21 |      187 |       70 |  Ì       |
|   58 | sub58   | sub58     |    21 |      158 |       58 |  F       |  
|   59 | sub59   | sub59     |    26 |      175 |       70 |  M       |   
|   60 | sub60   | sub60     |    24 |      183 |      107 |  M       |    
|   61 | sub61   | sub61     |    24 |      170 |       70 |  M       |   
|   62 | sub62   | sub62     |    20 |      180 |       70 |  M       |    
|   63 | sub63   | sub63     |    24 |      187 |       85 |  M       |  
|   64 | sub64   | sub64     |    26 |      181 |       70 |  M       |   
|   65 | sub65   | sub65     |    40 |      170 |      100 |  M       |    
|   66 | sub66   | sub66     |    20 |      193 |       83 |  M       |    
|   67 | sub67   | sub67     |    23 |      180 |       67 |  M       |  
+------+---------+-----------+-------+----------+----------+----------+


Activities of Daily Living:
+----+-------+----------------------------+--------+----------+---------------------------------------------------+
| No.| Label | Activity                   | Trials | Duration | Description                                       |
+----+-------+----------------------------+--------+----------+---------------------------------------------------+
| 1  | STD   | Standing                   | 1      | 5min     | Standing with subtle movements                    |
| 2  | WAL   | Walking                    | 1      | 5min     | Normal walking                                    |
| 3  | JOG   | Jogging                    | 3      | 30s      | Jogging                                           |
| 4  | JUM   | Jumping                    | 3      | 30s      | Continuous jumping                                |
| 5  | STU   | Stairs up                  | 6      | 10s      | Stairs up (10 stairs)                             |
| 6  | STN   | Stairs down                | 6      | 10s      | Stairs down (10 stairs)                           |
| 7  | SCH   | Stand to sit(sit on chair) | 6      | 6s       | Transition from standing to sitting               |
| 8  | SIT   | Sitting on chair           | 1      | 1min     | Sitting on a chair with subtle movements          |
| 9  | CHU   | Sit to stand(chair up)     | 6      | 6s       | Transition from sitting to standing               |
| 10 | CSI   | Car-step in                | 6      | 6s       | Step in a car                                     |
| 11 | CSO   | Car-step out               | 6      | 6s       | Step out a car                                    |
| 12 | LYI   | Lying                      | 12     | -        | Activity taken from the lying period after a fall |
+----+-------+----------------------------+--------+----------+---------------------------------------------------+


Falls:
+----+-------+--------------------+--------+----------+---------------------------------------------------------+
| No.| Label | Activity           | Trials | Duration | Description                                             |
+----+-------+--------------------+--------+----------+---------------------------------------------------------+
| 10 | FOL   | Forward-lying      | 3      | 10s      | Fall Forward from standing, use of hands to dampen fall |
| 11 | FKL   | Front-knees-lying  | 3      | 10s      | Fall forward from standing, first impact on knees       |
| 12 | BSC   | Back-sitting-chair | 3      | 10s      | Fall backward while trying to sit on a chair            |
| 13 | SDL   | Sideward-lying     | 3      | 10s      | Fall sidewards from standing, bending legs              |
+----+-------+--------------------+--------+----------+---------------------------------------------------------+

Scenarios:
+---------------------------------------------------------------------------------------------+
| 1st Scenario of Leaving the Home (SLH), Total duration 125’’ at max (1 trial/participant)   |
+----+-------+--------------------+-----------------------------------------------------------+
| No.| Label | Activity           | Description                                               |
+----+-------+--------------------+-----------------------------------------------------------+
| 1  | STD   | Standing           |  The recording starts with the participant standing       |
| 2  | WAL   | Walking            |  outside the door and locking the door. Then walks        |
| 3  | STN   | Stairs down        |  and descent stairs to leave his home. Following, he      |
| 4  | WAL   | Walking            |  riches the parking area where he stands in front of the  |
| 5  | STD   | Standing           |  car, unlocks the lock of the car, opens the door and     |
| 6  | CSI   | Car-step in        |  gets in the car. He remains sited for some seconds,      |
| 7  | SIT   | Sitting on chair   |  then he gets out of the car, closes the door and stands  |
| 8  | CSO   | Car-step out       |  in front of the door to lock the car.                    |
| 9  | STD   | Standing           |                                                           |
+-----+------+--------------------+-----------------------------------------------------------+
| 2nd Scenario of Being at work (SBW), Total duration 185’’ at max (1 trial/participant)      |
+----+-------+--------------------+-----------------------------------------------------------+
| No.| Label | Activity           | Description                                               |
+----+-------+--------------------+-----------------------------------------------------------+
| 1  | STD   | Standing           |  The recording starts with the participant standing       |
| 2  | WAL   | Walking            |  outside the cars door. Then walks from the parking       |
| 3  | STU   | Stairs up          |  area to his work building. He walks and ascent stairs    |
| 4  | WAL   | Walking            |  till he riches his office where he stops in front of the |
| 5  | STD   | Standing           |  door. Once he finds the keys he opens the door, gets     |
| 6  | WAL   | Walking            |  in his office and walks to his chair, where he sits.     |
| 7  | SCH   | Stand to sit       |                                                           |
| 8  | SIT   | Sitting on chair   |                                                           |
+-----+------+--------------------+-----------------------------------------------------------+
| 3rd Scenario of Leaving work (SLW), Total duration 185’’ at max (1 trial/participant)       |
+----+-------+--------------------+-----------------------------------------------------------+
| No.| Label | Activity           | Description                                               |
+----+-------+--------------------+-----------------------------------------------------------+
| 1  | SIT   | Sitting on chair   |  The recording starts with the participant sitting in the |
| 2  | CHU   | Sit to stand       |  chair in his office area. Then he gets up from the       |
| 3  | WAL   | Walking            |  chair, walks to the door and stands outside the office   |
| 4  | STD   | Standing           |  door. Once he find the keys, he lock the door and        |
| 5  | WAL   | Walking            |  walks and descent stairs till he riches the parking      |
| 6  | STN   | Stairs down        |  area. He walks to his car and stands in front of the     |
| 7  | WAL   | Walking            |  car, unlocks the lock of the car, opens the door and     |
| 8  | STD   | Standing           |  gets in the car. He remains sited for some seconds,      |
| 9  | CSI   | Car-step in        |  then he gets out of the car, closes the door and stands  |
| 10 | SIT   | Sitting on chair   |  in front of the door to lock the car.                    |
| 11 | CSO   | Car-step out       |                                                           |
| 12 | STD   | Standing           |                                                           |
+----+-------+--------------------+-----------------------------------------------------------+
| 4th Scenario of Being Exercise (SBE), Total duration 125’’ at max (1 trial/participant)     |
+----+-------+--------------------+-----------------------------------------------------------+
| No.| Label | Activity           | Description                                               |
+----+-------+--------------------+-----------------------------------------------------------+
| 1  | STD   | Standing           |  The recording starts with the participant standing in    |
| 2  | WAL   | Walking            |  front of the car. He starts his exercise by walking,     |
| 3  | JOG   | Jogging            |  then starts jogging from some seconds and once again     |
| 4  | WAL   | Walking            |  walking. Then he stops for some seconds to get a         |
| 5  | STD   | Standing           |  breath and he starts jumping and once more he            |
| 6  | JUM   | Jumping            |  standing to relax a little. Finally he walks till his    |
| 7  | STD   | Standing           |  car and stands outside the door.                         |
| 8  | WAL   | Walking            |                                                           |
| 9  | STD   | Standing           |                                                           |
+----+-------+--------------------+-----------------------------------------------------------+
| 5th Scenario of Returning at Home (SRH), Total duration 155’’ at max (1 trial/participant)  |
+----+-------+--------------------+-----------------------------------------------------------+
| No.| Label | Activity           | Description                                               |
+----+-------+--------------------+-----------------------------------------------------------+
| 1  | STD   | Standing           |  The recording starts with the participant standing       |
| 2  | CSI   | Car-step in        |  outside the cars door. He unlocks the lock of the car,   |
| 3  | SIT   | Sitting on chair   |  opens the door and gets in the car. He remains sited     |
| 4  | CSO   | Car-step out       |  for some seconds, then he gets out of the car, closes    |
| 5  | STD   | Standing           |  the door and stands in front of the door to lock the     |
| 6  | WAL   | Walking            |  car.  Then walks from the parking area to his home.      |
| 7  | STU   | Stairs up          |  He walks and ascent stairs till riches his home door,    |
| 8  |  WAL  | Walking            |  where he stands to finds the keys. Then he opens the     |
| 9  | STD   | Standing           |  door, gets in his home, walks till a chair and sits.     |
| 10 | WAL   | Walking            |                                                           |
| 11 | SCH   | Stand to sit       |                                                           |
+----+-------+--------------------+-----------------------------------------------------------+


Sensors:
+------+---------------+----------------------------------------------------+--------------------------------------------------------------+
| Code | Type          | Values                                             | Description                                                  |
+------+---------------+----------------------------------------------------+--------------------------------------------------------------+
| acc  | accelerometer | timestamp(ns),x,y,z(m/s^2)                         | Acceleration force along the x y z axes (including gravity). |
| gyro | gyroscope     | timestamp(ns),x,y,z(rad/s)                         | Rate of rotation around the x y z axes (Angular velocity).   |
| ori  | orientation   | timestamp(ns),Azimuth,Pitch,Roll(degrees)          | Angle around the z x y axes.                                 |
+------+---------------+----------------------------------------------------+--------------------------------------------------------------+

Related work: 
 • Chatzaki C., Pediaditis M., Vavoulas G., Tsiknakis M. (2017) 
   Human Daily Activity and Fall Recognition Using a Smartphone’s Acceleration Sensor. 
   In: Rocker C., O'Donoghue J., Ziefle M., Helfert M., Molloy W. (eds) 
   Information and Communication Technologies for Ageing Well and e-Health. ICT4AWE 2016.
   Communications in Computer and Information Science, vol 736, pp 100-118.
   Springer, Cham, DOI 10.1007/978-3-319-62704-5_7
 
 •  Chatzaki, C., Pediaditis, M., Vavoulas, G. and Tsiknakis, M., 
    "Estimating normal and abnormal activities using smartphones",
    In Proceedings of the 13th International Conference on Wearable Micro and Nano Technologies for Personalised Health (pHealth),
	v.224, pp 195-200,29-31 May 2016, Heraklion, Crete, Greece,  DOI:10.3233/978-1-61499-653-8-195

 •  Chatzaki Charikleia, 
	"Estimating human activity patterns in dynamic environments based on smart, wearable sensors : a feasibility study",
	 M.Sc. Thesis , Dept. Informatics Enginnering,Heraklion, Crete, Greece, 2016
	
 •  Vavoulas, G., Chatzaki, C., Malliotakis, T., Pediaditis, M. and Tsiknakis, M., 
    "The MobiAct Dataset: Recognition of Activities of Daily Living using Smartphones",
    In Proceedings of the International Conference on Information and Communication Technologies for Ageing Well and e-Health (ICT4AWE 2016),
    vol. 1, pp 143-151,ISBN: 978-989-758-180-9, DOI: 10.5220/0005792401430151

 •  G. Vavoulas, M. Pediaditis, C. Chatzaki, E. G. Spanakis, M. Tsiknakis, 
    "The MobiFall Dataset: Fall Detection and Classification with a Smartphone", 
    invited publication for the International Journal of Monitoring and Surveillance Technologies Research,
    pp 44-56, 2014, DOI:10.4018/ijmstr.2014010103
	
 •  G. Vavoulas, M. Pediaditis, E. Spanakis, M. Tsiknakis,
    "The MobiFall Dataset: An Initial Evaluation of Fall Detection Algorithms Using Smartphones",
	6th IEEE International Symposium on Monitoring & Surveillance Research (ISMSR): Healthcare-Bioinformatics, 
	Chania, Greece, 2013, DOI:10.1109/BIBE.2013.6701629
	
====================================================================
