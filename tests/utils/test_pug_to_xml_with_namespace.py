from pathlib import Path
from reportgen.utils import pug_to_xml as pug, xml_to_dict as xml

ROOT = Path(__file__).parent
DATA = ROOT.joinpath('data')


def test_data():
    data_xml = xml.from_file(DATA.joinpath('report_with_namespace.xml'), 'abdera')
    data = pug.build_data(data_xml)
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe", "nfe2": "http://www.portalfiscal.inf.br/nfe2"}

    data = pug._data_with_namespace(data, ns)

    assert data.nfeProc.nfe__NFe.infNFe['@Id'] == 'NFe0001'
    assert data.nfeProc.nfe__NFe.infNFe.ide.cUF['$'] == '35'
    assert data.nfeProc.nfe2__NFe.infNFe['@Id'] == 'NFe0002'
    assert data.nfeProc.nfe2__NFe.infNFe.ide.cUF['$'] == '36'
