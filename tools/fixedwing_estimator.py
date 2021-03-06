"""
1、计算飞机转弯半径
https://wenku.baidu.com/view/2a3c1cd7240c844769eaee5b.html
真空速TAS
转弯坡度α
转弯率ω
转弯半径R
重力加速度g
转弯半径R=TAS²/(tanα×g)  = TAS/（2πω）

飞行员执照考试题：
飞机进近时，规定的标准转弯率是3 deg/s
注意:
（1）
速度为真空速（静风条件下真空速与地速相同），
应换算成米/秒，
1节=1.852公里/小时=0.514米/秒,
计算出来的转弯半径单位为米。
(2)
真空速与指示空速的简单换算公式：
TAS = IAS * （P / P0）^ 0.5
IAS : 指示空速
P   ：当前外界气压值
P0  ：标准海平面气压值
(3)
tan15 = 0.268
tan25 = 0.466
tan30 = 0.577

飞机相对地面的转弯半径还跟风的来向和大小有关，
会影响相对地面的实际转弯轨迹
"""
