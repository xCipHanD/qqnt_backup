# qqnt_backup
qqnt 数据库解密项目

## 关于
适用于Android_NT_QQ数据库解密。

## 使用
1. 通过备份app/使用具有root权限的安卓模拟器/root真机获取对数据库的访问权限。
2. 从``/data/user/0/com.tencent.mobileqq/files/uid/``处找到``qq号###qquid``的文件，记录下对应的``qquid``。
3. 计算32位``hash``, 规则为 ``hash = md5( md5(qquid) + "nt_kernel" )``
4. 将目录``/data/user/0/com.tencent.mobileqq/databases/nt_db/nt_qq_{32位hash}``打包。
5. 将解压后的目录与``decrypt.py``脚本放在同一目录下，填入参数，运行后将生成解密文件。
6. 若解密失败，请检查适用范围及参数是否正确。

## 免责声明
本项目仅供学习交流使用，严禁用于任何违反中国大陆法律法规、您所在地区法律法规、QQ软件许可及服务协议的行为，开发者不承担任何相关行为导致的直接或间接责任。

本项目不对生成内容的完整性、准确性作任何担保，生成的一切内容不可用于法律取证，您不应当将其用于学习与交流外的任何用途。

## 致谢
https://github.com/QQBackup/qq-win-db-key