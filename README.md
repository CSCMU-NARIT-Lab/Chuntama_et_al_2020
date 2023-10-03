# Chuntama_et_al_2020
Multiclass_Classification_of_Astronomical_Objects_in_the_Galaxy_M81_using_Machine_Learning_Techniques

Software Version
Weka 3.8.4 

Libary install
- pip install pandas
- pip install -U scikit-learn

Remark name of class SF = FO 

Step Run file 
1. Convert .cat file to .reg file using #CatToReg.py for marking Objects on pictures
2. ให้ทางนักดาราศาสตร์ของสถาบันวิจัยดาราศาสตร์แห่งชาติ(NARIT) ทำการระบุคลาสของ Object ที่อยู่ในรูปภาพเพื่อทำการติด Label ให้กับข้อมูล
3. ทำการ Mapping Data ที่ติด Label โดยใช้พิกัด รันไฟล์ #matchRegFile.py
4. เนื่องจากต้องการให้ข้อมูล training dataset และ test dataset มีข้อมูลของทุกๆคลาส class ของแต่ละรูปด้วย #CategorizeClass.py ก่อนที่จะแบ่งข้อมูลด้วยการรัน #randomDATAtoModel.py
5. หากข้อมูลมีหลายรูปต้องทำการรัน #mergeTrainTest.py เพื่อที่จะรวมข้อมูล train test ของแต่ละรูปเข้าด้วยกัน

Model ที่ถูก train แล้ว ถูกจัดเก็บอยู่ใน folder model

Source test file => \region5,14,23,32\pic23\seed17\datatest.csv.arff สามารถใช้ .arff เพื่อรันใน weka ได้เลย

หากนำ Code หรือ ข้อมูลไปใช้ กรุณาอ้างอิง paper 
T. Chuntama, P. Techa-Angkoon, C. Suwannajak, B. Panyangam, and
N. Tanakul, “Multiclass Classification of Astronomical Objects in the
Galaxy M81 using Machine Learning Techniques,” Proceedings of
The 24th International Computer Science and Engineering
Conference (ICSEC2020), pp. 1-6, Dec 2020.