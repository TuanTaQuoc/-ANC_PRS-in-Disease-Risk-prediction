Dự án học phần Đồ án Nghiên Cứu Cử Nhân , Sinh viên : Tạ Quốc Tuấn , MSSV : 20225110

 Mô tả chi tiết quy trình xử lý dữ liệu Genotype cho bộ dữ liệu ADNI:

 - Công nghệ sử dụng : PLINK 1.9 , TOPMED Imputation Server
 - Tập dữ liệu ban đầu : Các file PLINK thô được thu thập từ bộ dữ liệu ADNI . Các file trên lần lượt được chia thành 4 phase khác nhau, lần lượt là ADNI1 , ADNIGO , ADNI2 , ADNI3 . 
  Quy trình xử lý bao gồm các giai đoạn sau :
  Giai đoạn 1 : Kiểm soát chất lượng cơ bản
  B1 : Thực hiện các cá thể có tỷ lệ thiếu dữ liệu cao
    Điều kiện giữ lại : Tỷ lệ genotype > 95%
  Lệnh :
```bash
          plink \
         --bfile ADNI_GO2_GWAS_2nd_orig_BIN \
         --mind 0.05 \
         --make-bed \
         --out ADNI_GO2_2nd_step1_indQC
```
  B2 : Thực hiện các biến thể có tỷ lệ thiếu dữ liệu cao
    Điều kiện giữ lại : Tỷ lệ Sample > 80%
  Lệnh : 
```bash
         plink \
         --bfile ADNI_GO2_2nd_step1_indQC \
         --geno 0.20 \
         --make-bed \
         --out ADNI_GO2_2nd_step2_indQC
```
  B3 : Tính toán tần số allele của bộ dữ liệu để chuẩn bị tham chiếu với 1 panel tham chiếu (HRC hoặc 1000G). Việc tham chiếu sẽ giúp ta phát hiện được tần suất sợi thuận và sợi nghịch trong bộ dữ liệu.

  Lệnh : 
```bash 
       plink --freq --bfile ADNI_GO2_2nd_step2_indQC --out ADNI_GO2_2nd_freq 
```

  B4 : Thực hiện kiểm tra tính nhất quán của dữ liệu gen với một panel tham chiếu . Đây là bước quan trọng nhất để đảm bảo dữ liệu của bạn khớp với panel tham chiếu (HRC/1000G) về:
         + Strand: Đảm bảo SNP đang ở chiều forward (+).
         + Alleles: Đảm bảo Ref/Alt allele khớp với tham chiếu.
         + Position: Đảm bảo vị trí bp khớp với bản build (thường là GRCh37/hg19).
    - B4.1 : Chạy script kiểm tra , sử dụng script HRC-1000G-check-bim.pl để đối chiếu file bim và frq với file tham chiếu HRC
       Lệnh : 
```bash      
            perl HRC-1000G-check-bim.pl \
              -b ADNI3_Final_QC.bim \
              -f ADNI3_Final_freq.frq \
              -r HRC.r1-1.GRCh37.wgs.mac5.sites.tab \
              -h
```
       Sau khi chạy lệnh trên , nó sẽ phân tích và tạo ra một shell script tên là Run-plink.sh (hoặc tên tương tự). Script này chứa các lệnh PLINK để:
             + Loại bỏ SNP không khớp vị trí hoặc allele.
             + Lật (flip) các SNP bị sai chiều (strand).
             + Cập nhật tên/ID của SNP cho chuẩn.
             + Cập nhật Allele tham chiếu.
    - B4.2 : Chạy file script sửa lỗi
       Lệnh : 
```bash
       sh Run-plink.sh
```
       Kết quả: Tạo ra các file PLINK mới được chia theo từng chromosome (thường có hậu tố -updated hoặc tương tự) đã được đồng bộ hóa với panel tham chiếu HRC.
  B5 : Chuyển đổi sang định dạng VCF để đưa lên TOPMED Imputation Server
     Lệnh :
```bash    
           * input_file="ADNI2_OmniEx_QC-updated-chr22"
              plink --bfile $input_file \
                    --a2-allele ${input_file}.bim 5 2 \
                    --recode vcf bgz \
                    --out chr22_temp \
                    --real-ref-alleles
            * Sắp xếp VCF files
            bcftools sort chr22_temp.vcf.gz -Oz -o chr22_upload.vcf.gz
            * Tạo file chỉ mục
            bcftools index chr22_upload.vcf.gz
```
    Thực hiện đầy đủ với 22 file NST
  Sau khi thực hiện xong 5 bước trên , ta thu được các file có định dạng chrk_upload.vcf.gz với k = {1,22} , ta sẽ tiến hành upload các file này lên TOPMED cho bước phasing và imputation

  Giai đoạn 2 : Phasing và Imputation trên TOPMED
     Đường link TOPMED Imputation Server : https://imputation.biodatacatalyst.nhlbi.nih.gov

     - Thực hiện tạo tài khoản và vào mục Run -> Genotype Imputation
     - Chọn Reference Panel : TOPMED r3 (latest) ; Input files là các file chr_upload.vcf.gz , lưu ý với mỗi job thì chỉ nên thực hiện trên một chromosome.
     - Array Build : hg19 ; rsq Filter : Off ; Phasing Engine : Eagle 2.4 ; Mode : QC & Imputation ;

     Sau khi job chạy xong sẽ trả về một file zip kèm mật khẩu giải nén, ta thực hiện giải nén file zip thì sẽ thu được 1 file chrk.dose.vcf.gz . Đây là file genotype sau quá trình nội suy.

     Như vậy với 4 phase và mỗi phase được xử lý sẽ gồm 22 file vcf, tổng cộng sẽ cần phải chạy xong 88 job.

     Chú ý :
       + Mỗi tài khoản chỉ được chạy tối đa 3 job cùng lúc.
       + Server có thể xử lý nhiều job cùng nhau tại một thời điểm , dẫn đến việc xử lý có thể bị lâu và job của mình sẽ phải vào hàng chờ.
       + Thông báo mới của TOPMED : Sắp tới TOPMED sẽ không hỗ trợ tạo tài khoản với các email được cung cấp miễn phí (VD : ...@gmail.com) . 



  Giai đoạn 3 : Hậu xử lý dữ liệu đã nội suy
    Công cụ : bcftools , PLINK 1.9
    Môi trường : Terminal trên Ubuntu
    B1 : Lọc các biến thể có chất lượng nội suy kém (R2 < 0.4)
```bash
     Lệnh : bcftools filter -i 'R2>=0.4' chr22.dose.vcf.gz -O z -o chr22.filtered.vcf.gz
```

    B2 : Annotate rsID theo file dbSNP v156 (latest)

    Link tải bản dbSNP v156 latest:
        https://ftp.ncbi.nih.gov/snp/latest_release/VCF/GCF_000001405.40.gz
    Lệnh : 
```bash
      for i in {1..22}
         do
         echo "--- Đang xử lý: chr${i} ---"
         bcftools annotate --rename-chrs rename_chrs.txt \
                           -a GCF_000001405.40.gz \
                           -c ID \
                           -Oz -o chr${i}.annotated.vcf.gz \
                           chr${i}.filtered.vcf.gz
        Done
``` 
    B3 : Làm sạch biến thể
    Sau khi có rsID, quy trình tiến hành lọc lấy các SNP chất lượng cao, lưỡng hình (Biallelic) và loại bỏ các dòng trùng lặp

    Lệnh :
```bash
      for i in {1..22}
         do
         # Lọc Biallelic SNP và loại bỏ trùng lặp (Normalization)
         bcftools view -v snps -m2 -M2 -i 'ID!="."' chr${i}.annotated.vcf.gz | \
         bcftools norm -d all -Oz -o chr${i}.matched.vcf.gz

         # Tạo chỉ mục (Index) cho file đã làm sạch
         bcftools index -t chr${i}.matched.vcf.gz
         done
```
    B4 : Hợp nhất dữ liệu
     Chuyển đổi các file VCF đã làm sạch sang định dạng nhị phân PLINK (.bed, .bim, .fam) và gộp 22 nhiễm sắc thể thành một bộ dữ liệu duy nhất

     Lệnh : 
```bash
       + Chuyển sang PLINK
       for i in {1..22}
         do
          plink --vcf chr${i}.match.vcf.gz --double-id --make-bed --out temp_chr${i}
         done
       + Gộp file
        -- Tạo danh sách gộp
        ls -v temp_chr*.bed | sed 's/.bed//' | tail -n +2 > merge_list.txt
        -- Gộp các chr còn lại vào chr1
        plink --bfile temp_chr1 --merge-list merge_list.txt --make-bed --out adni_merged_full
```
    B5 : Lọc các allele có tần suất thấp (MAF > 0.01)

    Lệnh : 
```bash  
    plink --bfile adni_merged_full --maf 0.01 --make-bed --out adni_maf01
```

    B6 : Thực hiện kiểm tra các mẫu trùng từ IBD
      B6.1 : Loại bỏ các SNP liên kết chặt chẽ để tính IBD (R2 < 0,2)
         Lệnh : 
```bash
    plink --bfile adni_maf01 --indep-pairwise 50 5 0.2 --out pruning_out
```
      B6.2 : Trích xuất dữ liệu phục vụ tính IBD
         Lệnh : 
```bash      
         plink --bfile adni_maf01 --extract pruning_out.prune.in --make-bed --out adni_for_IBD
```
      B6.3 : Ước tính giá trị IBD
         Lệnh :
```bash 
    plink --bfile adni_for_IBD --genome --out adni_ibd_result
```
      B6.4 : Lọc mẫu vi phạm bằng lệnh awk
         Lệnh : 
```bash
    awk '$10 > 0.90 {print $2, $4, $10}' adni_ibd_result.genome
```
    Sau bước này , nếu như trong bộ dữ liệu tồn tại 2 bô gen có khả năng cao là cùng một người (IBD cao) , chương trình sẽ lập danh sách các RID đó để báo cáo cho chúng ta. Ta sẽ thực hiện loại bỏ các mẫu trùng bằng lệnh --remove.







***PS : Các đường link tới các bộ dữ liệu đã xử lý
   - Dữ liệu PLINK gốc của bộ ADNI và tệp chứa thông tin lịch sử khám bệnh : https://drive.google.com/drive/folders/1g9As2FH68_v9ZZUJjJuTBBUSi6ppyOSF?hl=vi
   - Dữ liệu PLINK sau khi đã được phân pha và nội suy trên TOPMed Imputation Server (Bao gồm các file zip và mật khẩu giải nén) : https://drive.google.com/drive/folders/1ninX676Jm_CqybJJHAYFrqYR4hPu462S?hl=vi
   - Dữ liệu genotype sau khi đã qua quy trình hậu xử lý, được lưu trữ dưới định dạng PLINK : https://drive.google.com/drive/folders/1Sw2PJgTEwaDYb4ipe0D09Pwpc3nYeXGR?hl=vi 
   **** Nếu có nhu cầu tải xuống các tập dữ liệu với mục đích nghiên cứu , vui lòng gửi request cho tôi ****


  