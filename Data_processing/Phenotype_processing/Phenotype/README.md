Quy trình xử lý và trích xuất dữ liệu kiểu hình (Phenotype)

- Chia tập DXSUM thành 4 file con theo từng Phase : ADNI1 , ADNIGO , ADNI2 , ADNI3
- Với từng phase :
   + Sắp xếp file theo RID bệnh nhân , nếu có các hàng có RID trùng nhau , sắp xếp theo Examdate tăng dần.
   + Lọc và chỉ giữ lại thông tin của các cột : Phase , ID , RID , PTID , Examdate và các cột sau đối với từng phase :
      *ADNI1 : DXCURRENT
      * ADNI2/GO : DXCHANGE
      * ADNI3 : Diagnosis
  + Tạo thêm 1 cột Phenotype với quy ước sau đây
      *ADNI1 : Phenotype = DXCURRENT
 * ADNI2/GO : DXCHANGE 1=Stable: NL to NL; 2=Stable: MCI to MCI; 3=Stable: Dementia to Dementia; 4=Conversion: NL to MCI; 5=Conversion: MCI to Dementia; 6=Conversion: NL to Dementia;
7=Reversion: MCI to NL; 8=Reversion: Dementia to MCI; 9=Reversion: Dementia to NL. Biểu diễn phenotype dưới dạng số với quy ước NL = 1 ; MCI = 2 ; Dementia = 3
 * ADNI3 : Phenotype = Diagnosis
  + Với từng giá trị RID , giữ lại hàng có giá trị Phenotype lớn nhất trong quá trình khám của bệnh nhân đó . Nếu như tồn tại nhiều hàng có giá trị lớn nhất bằng nhau , giữ lại hàng có Examdate gần nhất.
- Sau khi thực hiện xong việc lọc cho cả 4 file :
  + Gộp cả 4 file đã lọc thành 1 file duy nhất , đảm bảo thông tin về số lượng cột hay tên các cột của cả 4 file đều là như nhau để thuận tiện cho việc gộp.   Giả sử ta thu được file ex sau khi gộp
  + Thực hiện sort RID trong file ex , nếu có các hàng có RID trùng nhau , sắp xếp theo Examdate tăng dần.
  + Với từng giá trị RID , giữ lại hàng có giá trị Phenotype lớn nhất trong quá trình khám của bệnh nhân đó . Nếu như tồn tại nhiều hàng có giá trị lớn nhất bằng nhau , giữ lại hàng có Examdate gần nhất.  => ADNI_Phenotype.csv




