import random
import secrets
import string
from pypinyin import pinyin, Style

def generate_strong_password():
    """生成只包含字母和数字的强密码。"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(10))

def process_name(name):
    """处理名称，生成拼音形式的cn（全小写，无空格），并提取第一个拼音音节作为sn。"""
    if any('\u4e00' <= char <= '\u9fff' for char in name):
        full_pinyin = ''.join([y for x in pinyin(name, style=Style.NORMAL) for y in x])
        cn = full_pinyin.replace(' ', '').lower()
        sn = pinyin(name, style=Style.NORMAL)[0][0]
    else:
        cn = name.lower().replace(' ', '')
        sn = cn
    return cn, sn

def read_names(file_path, num_users=20):
    """从指定文件中随机选择指定数量的用户名，确保使用utf-8编码读取文件。"""
    with open(file_path, 'r', encoding='utf-8') as file:
        all_names = file.read().splitlines()
    return random.sample(all_names, num_users)

def main():
    file_path = 'names.txt'
    num_users = 15
    names = read_names(file_path, num_users)
    passwords = ['1qaz2wsx'] * 2 + ['admin123'] * 2 + ['123456'] * 3 + ['password'] * 3 + ['1qaz2wsx'] * 4 + [generate_strong_password() for _ in range(num_users - 9)]
    random.shuffle(passwords)

    # 处理名字并创建 LDAP 条目
    users_data = []
    for name in names:
        cn, sn = process_name(name)
        password = passwords.pop()
        users_data.append((cn, cn, sn, password))  # 使用 cn 作为 uid

    # 随机选择两名用户加入管理组，一名加入 HR 组
    manage_group_members = random.sample(users_data, 2)
    remaining_users = [user for user in users_data if user not in manage_group_members]
    hr_group_member = random.choice(remaining_users)

    # 生成 LDIF 内容
    ldif_content = "dn: ou=users,dc=example,dc=com\n"
    ldif_content += "objectClass: organizationalUnit\n"
    ldif_content += "ou: users\n\n"
    ldif_content += "dn: ou=groups,dc=example,dc=com\n"
    ldif_content += "objectClass: top\n"
    ldif_content += "objectClass: organizationalUnit\n"
    ldif_content += "ou: groups\n"
    ldif_content += "description: Container for groups\n\n"
    ldif_content += "dn: cn=manage,ou=groups,dc=example,dc=com\n"
    ldif_content += "objectClass: groupOfUniqueNames\n"
    ldif_content += "cn: manage\n"
    for cn, uid, sn, password in manage_group_members:
        uid_str = f"uid={uid},ou=users,dc=example,dc=com"
        ldif_content += f"uniqueMember: {uid_str}\n"

    ldif_content += "\n"
    ldif_content += "dn: cn=hr,ou=groups,dc=example,dc=com\n"
    ldif_content += "objectClass: groupOfUniqueNames\n"
    ldif_content += "cn: hr\n"
    uid_str = f"uid={hr_group_member[1]},ou=users,dc=example,dc=com"
    ldif_content += f"uniqueMember: {uid_str}\n\n"

    for uid, cn, sn, password in sorted(users_data, key=lambda x: x[0]):
        uid_str = f"uid={uid},ou=users,dc=example,dc=com"
        ldif_content += f"dn: {uid_str}\n"
        ldif_content += "objectClass: inetOrgPerson\n"
        ldif_content += f"cn: {cn}\n"
        ldif_content += f"sn: {sn}\n"
        ldif_content += f"uid: {uid}\n"
        ldif_content += f"userPassword: {password}\n\n"

    # 写入文件
    with open('users.ldif', 'w', encoding='utf-8') as file:
        file.write(ldif_content)
    print("LDIF content has been written to users.ldif with manage and hr groups")

if __name__ == "__main__":
    main()
