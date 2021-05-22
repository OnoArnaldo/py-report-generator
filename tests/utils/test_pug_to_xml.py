from reportgen.utils import pug_to_xml as pug


def test_data_is_string():
    data = pug.build_data('The Name')
    assert data['$'] == 'The Name'


def test_data_value_in_children():
    data = pug.build_data({'children': ['The Name']})
    assert data['$'] == 'The Name'


def test_data_attribute():
    data = pug.build_data({'attributes': {'id': 'ID0001'}})
    assert data['@id'] == 'ID0001'


def test_data_list():
    data = pug.build_data([
        {'children': ['I0001'], 'attributes': {'id': 'ID0001'}},
        {'children': ['I0002'], 'attributes': {'id': 'ID0002'}},
        {'children': ['I0003'], 'attributes': {'id': 'ID0003'}},
    ])

    items = data['*']
    assert len(items) == 3
    assert items[0]['$'] == 'I0001'
    assert items[0]['@id'] == 'ID0001'


def test_data_value_chain():
    data = pug.build_data({
        "company": {
          "children": [
            {
              "name": {
                "attributes": {"id": "Comp0001", "alias": "Company A"},
                "children": ["The Company"]
              }
            },
            {"address": "The Address"},
            {"email": "test@email.com"},
            {"phone": "1234.5678"}
          ]
        }
      })

    assert data.company.address['$'] == 'The Address'
    assert data.company.name['$'] == 'The Company'
    assert data.company.name['@id'] == 'Comp0001'
    assert data.notExists['$'] == ''
    assert data.notExists['@id'] == ''
    assert data.notExists.nothing['$'] == ''
    assert data.notExists.nothing['@id'] == ''


def test_data_chain_with_list():
    data = pug.build_data({
        'document': {'children': [
            {
                "item": {
                    "attributes": {"id": "i002"},
                    "children": [
                        {"name": "Item002"},
                        {"qty": "20"},
                        {"price": "2000"}
                    ]}
            },
            {
                "item": {
                    "attributes": {"id": "i003"},
                    "children": [
                        {"name": "Item003"},
                        {"qty": "30"},
                        {"price": "3000"}
                    ]}
            }]}})

    assert data.document.item['*'][0].name['$'] == 'Item002'
