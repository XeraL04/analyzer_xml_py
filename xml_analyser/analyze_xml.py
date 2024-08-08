from lxml import etree
from collections import Counter
import os

def analyze_large_xml(file_path):
    context = etree.iterparse(file_path, events=('start', 'end'))
    context = iter(context)
    
    # Get the root element
    event, root = next(context)

    # Function to capture the structure of the XML
    def get_structure(elem, level=0):
        structure = '  ' * level + str(elem.tag) + str(elem.attrib) + '\n'
        for child in elem:
            structure += get_structure(child, level + 1)
        return structure

    xml_structure = get_structure(root)
    tag_counter = Counter()

    # Extract specific tag values and count tags
    # your_tag_values = []

    # for event, elem in context:
    #     if event == 'end':
    #         # Count the tags
    #         tag_counter[elem.tag] += 1
    #         # Extract values of specific tags
    #         if elem.tag == 'your_tag':  # Replace 'your_tag' with your specific tag
    #             your_tag_values.append(elem.text)
    #         # Clear the processed element to free memory
    #         root.clear()

    # Create a directory to store the output file
    output_dir = 'analyzed_xml'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the output file name
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    output_file_path = os.path.join(output_dir, f"{file_name}_analysis_results.txt") 

    # Save the results to a file
    with open(output_file_path, 'w') as file:
        file.write("XML Structure:\n")
        file.write(xml_structure + '\n')
        
        # file.write("\nValues of 'your_tag':\n")
        # for value in your_tag_values:
        #     file.write(str(value) + '\n')
        
        file.write("\nTag Counts:\n")
        file.write(str(tag_counter) + '\n')

    print(f"Analysis results saved to {output_file_path}")

if __name__ == "__main__":
    analyze_large_xml(r'path/to/the/file')
