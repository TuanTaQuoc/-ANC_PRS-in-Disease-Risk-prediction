import pandas as pd
import os

raw_file = 'ADNI1_ML_1e8.raw'   
pheno_file = 'ADNI_Phenotype.csv' 
output_file = 'Dataset_ADNI1_1e8_Final.csv'

if not os.path.exists(raw_file):
    print(f"Lỗi: Không tìm thấy file {raw_file}. Hãy kiểm tra lại lệnh PLINK.")
    exit()

print("Đang tải dữ liệu Genotype và Phenotype...")
df_geno = pd.read_csv(raw_file, sep=r'\s+')
df_pheno = pd.read_csv(pheno_file)

# 2. TRÍCH XUẤT MÃ BỆNH NHÂN (RID)
def extract_rid(iid_string):
    try:
        return int(str(iid_string)[-4:])
    except:
        return None

df_geno['RID'] = df_geno['IID'].apply(extract_rid)

# 3. LỌC VÀ LÀM SẠCH CỘT
snp_cols = [col for col in df_geno.columns if col.startswith('rs')]
df_geno_clean = df_geno[['RID'] + snp_cols]

# 4. GỘP DỮ LIỆU VỚI PHENOTYPE
df_final = pd.merge(df_geno_clean, df_pheno[['RID', 'Phenotype']], on='RID', how='inner')

print("Đang xử lý các giá trị khuyết thiếu (nếu có)...")
for col in snp_cols:
    if df_final[col].isnull().sum() > 0:
        df_final[col] = df_final[col].fillna(df_final[col].mode()[0])

# 5. XUẤT BÁO CÁO VÀ LƯU FILE
print("\n--- BÁO CÁO KẾT QUẢ ---")
print(f"Số lượng bệnh nhân (Samples): {df_final.shape[0]}")
print(f"Số lượng biến thể (Features): {len(snp_cols)}")
print("\nPhân bổ nhãn Phenotype (1.0 = Bình thường, 3.0 = Alzheimer):")
print(df_final['Phenotype'].value_counts().to_string())

df_final.to_csv(output_file, index=False)
print(f"\n[THÀNH CÔNG] Dữ liệu ML đã được lưu vào: {output_file}")