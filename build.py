import os
import json
import zipfile
import re

def load_asset_contents(asset_map, asset_dir):
    asset_contents = {}
    for key, filename in asset_map.items():
        file_path = os.path.join(asset_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            asset_contents[key] = f.read()
    return asset_contents

def create_zip_with_replace(source_dir, output_zip, replace_map, asset_contents, extra_files=None, image_dir=None):
    patterns = {f"${{{key}}}": value for key, value in replace_map.items() if key != 'asset'}
    
    for key, content in asset_contents.items():
        patterns[f"${{asset.{key}}}"] = content
    
    # ZIP内のルートディレクトリ名を決定（${NAME}の値を使用）
    zip_root_dir_name = replace_map.get("NAME", "output")

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # scriptディレクトリ内のファイルを処理（置換あり）、ZIP内では ${NAME}/... に配置
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 相対パスを取得し、ZIP内の新しい配置パスを構築
                relative_path_in_script = os.path.relpath(file_path, source_dir)
                zip_path = os.path.join(zip_root_dir_name, relative_path_in_script)

                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    for pattern, replacement in patterns.items():
                        content = content.replace(pattern, replacement)
                
                zipf.writestr(zip_path, content.encode('utf-8'))
        
        # imageディレクトリ内のファイルをそのまま追加（置換なし）、ZIPのルート直下に配置
        if image_dir and os.path.exists(image_dir):
            for root, dirs, files in os.walk(image_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # ここが変更点: imageフォルダからの相対パスをそのままZIP内のパスとする
                    relative_path_in_image = os.path.relpath(file_path, os.path.dirname(image_dir))
                    zipf.write(file_path, relative_path_in_image)

        # 追加ファイルをZIPのルートに格納（置換なし）
        if extra_files:
            for file_path in extra_files:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                else:
                    print(f"警告: {file_path} が見つかりませんでした。ZIPに追加されません。")

if __name__ == "__main__":
    SOURCE_DIR = "script"
    ASSET_DIR = "Asset"
    IMAGE_DIR = "image"
    REPLACE_JSON = "replace.json"
    EXTRA_FILES_TO_INCLUDE = ["LICENSE", "README.md"]

    with open(REPLACE_JSON, 'r', encoding='utf-8') as f:
        replace_data = json.load(f)
    
    project_name = replace_data.get("NAME", "output")
    project_version = replace_data.get("VERSION", "0.0.0")
    OUTPUT_ZIP = f"{project_name}_{project_version}.zip"

    asset_map = replace_data.get("asset", {})
    all_asset_contents = load_asset_contents(asset_map, ASSET_DIR)
    
    create_zip_with_replace(
        SOURCE_DIR, 
        OUTPUT_ZIP, 
        replace_data, 
        all_asset_contents,
        EXTRA_FILES_TO_INCLUDE,
        IMAGE_DIR
    )
