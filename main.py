from convert_data import convert_data_to_table
from get_data import get_data_from_libex
from get_url import get_url, get_user_id_part


def main():
    url = get_url()
    file_name = "./books_" + get_user_id_part(url) + ".xlsx"
    convert_data_to_table(get_data_from_libex(url), file_name)


if __name__ == "__main__":
    main()
