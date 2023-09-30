import csv
import struct
import sys

def convert_to_binary(input_csv, output_bin):
    with open(input_csv, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        
        # Lê a primeira linha para determinar o formato das variáveis
        header = next(reader)
        data_format = []

        for field in header:
            if field[0]>='0' and  field[0]<='9' and  '.' in field :
                data_format.append('f')  # float
            elif field[0]>='0' and  field[0]<='9':
                data_format.append('i')  # integer
            else:
                data_format.append('51s')  # string (51 characters)
        
        format_string = ''.join(data_format)
        
        with open(output_bin, 'wb') as bin_file:
            for row in reader:
                if len(row) != len(header):
                    print(f"Erro na linha {reader.line_num}: Número incorreto de campos.")
                    sys.exit(1)
                
                for i, field in enumerate(row):
                    if data_format[i] == 'i':
                        bin_file.write(struct.pack('i', int(field)))
                    elif data_format[i] == 'f':
                        bin_file.write(struct.pack('f', float(field)))
                    else:
                        # Preenche a string com espaços em branco e adiciona o caractere nulo no final
                        bin_field = field.ljust(50)[:50].encode('utf-8') + b'\x00'
                        bin_file.write(bin_field)
                
                bin_file.write(b'\n')  # Adiciona uma quebra de linha ao final de cada linha


print("\033c\033[44;37m\n")
if len(sys.argv) != 3:
    print("Uso: python programa.py arquivo_csv arquivo_binario")
    sys.exit(1)

input_csv = sys.argv[1]
output_bin = sys.argv[2]

convert_to_binary(input_csv, output_bin)
print(f"Conversão concluída. Saída gravada em {output_bin}")



