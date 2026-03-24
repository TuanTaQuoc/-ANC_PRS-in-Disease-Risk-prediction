- Các file cần thiết 
  + Các file PLINK sau khi đã qua quy trình xử lý genotype . Như em làm thì sẽ có 4 file PLINK riêng biệt, ứng với 4 phase của ADNI (ADNI1 , ADNI2Omni , ADNI2Go2nd , ADNI3). Trong báo cáo này, em tạm gọi các file này là PLINKADNI1;…
  + Các file chứa tên các biến thể có độ tương quan cao , lọc theo các mốc p-value (1e-4 ; 1e-6 ; 1e-8) từ metadata của Jansen (2019). Trong báo cáo này, em tạm gọi các file này là các file varp_1e-4.csv ;…..
  + File csv chứa thông tin RID và phenotype đã qua xử lý phenotype. Trong báo cáo này, em tạm gọi file này là phenotype.csv


- Quy trình : 
  + Thực hiện trích tên các biến thể trong các file varp_1e-4.csv;…  bằng lệnh awk:
```bash     
     awk -F, 'NR>1 {print $1}' varp_1e-8.csv > list_rsid_1e8.txt
```
  + Dùng PLINK lọc biến thể và tạo ra genotype dạng số

     Lệnh :
```bash
           plink --bfile adni1_final_qc \
                 --extract list_rsid_1e8.txt \
                 --recode A \
                 --out ADNI1_ML_1e8
```
Output : ADNI1_ML_1e8.raw
   + Thực hiện lọc và gộp dữ liệu phenotype bằng chương trình Python:
```bash
   python merge_ADNI.py
```
