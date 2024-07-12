import os
import shutil
import difflib
import stat

def copy_with_permissions(src, dest):
    if os.path.isdir(src):
        if not os.path.exists(dest):
            shutil.copytree(src, dest, copy_function=shutil.copy)
            shutil.copystat(src, dest)
        else:
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                copy_with_permissions(s, d)
    else:
        shutil.copy2(src, dest)

        # İzinleri kopyala
        st = os.stat(src)
        os.chown(dest, st.st_uid, st.st_gid)
        os.chmod(dest, st.st_mode)

# Klasör yolları
nfs1 = './nfs1'
nfs2 = './nfs2'

# nfs1 ve nfs2 içindeki klasör isimlerini al
nfs1_dirs = [d for d in os.listdir(nfs1) if os.path.isdir(os.path.join(nfs1, d))]
nfs2_dirs = [d for d in os.listdir(nfs2) if os.path.isdir(os.path.join(nfs2, d))]

# Benzer klasör isimlerini eşleştirme ve kopyalama
for dir1 in nfs1_dirs:
    # En benzer klasör ismini bul
    closest_match = difflib.get_close_matches(dir1, nfs2_dirs, n=1, cutoff=0.5)
    
    if closest_match:
        dir2 = closest_match[0]
        source_dir = os.path.join(nfs1, dir1)
        target_dir = os.path.join(nfs2, dir2)
        
        # Kaynak klasördeki dosyaları hedef klasöre kopyalar
        copy_with_permissions(source_dir, target_dir)
        
        print(f'Copied content from {source_dir} to {target_dir}')
