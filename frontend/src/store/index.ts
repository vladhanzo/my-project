with open(slice_path, "w", encoding="utf-8") as f:
    f.write(slice_code.strip())

with open(index_path, "w", encoding="utf-8") as f:
    f.write(store_code.strip())

# Подтвердим создание
os.listdir(store_dir)
Результат
['assemblySlice.ts', 'index.ts']