import pytest


class FakeCanvas:
    log = []
    ignore_in_getattr = ['setFont']

    def __init__(self, reference):
        self.reference = reference
        self._fontname: str
        self._fontsize: float

    def __getitem__(self, item):
        ref = object.__getattribute__(self, 'reference')
        ref = f'{ref}[{item}]'
        FakeCanvas.log.append([ref])
        return FakeCanvas(ref)

    def __setattr__(self, key, value):
        if key != 'reference':
            ref = object.__getattribute__(self, 'reference')
            FakeCanvas.log.append([f'{ref}.{key} = {value}'])
        object.__setattr__(self, key, value)

    def __getattribute__(self, item):
        try:
            ret = object.__getattribute__(self, item)
            if item not in FakeCanvas.ignore_in_getattr:
                ref = object.__getattribute__(self, 'reference')
                FakeCanvas.log.append([f'{ref}.{item}', ret])
            return ret
        except:
            ref = object.__getattribute__(self, 'reference')
            return FakeCanvas(f'{ref}/{item}')

    def __call__(self, *args, **kwargs):
        ref = object.__getattribute__(self, 'reference')
        ref = f'{ref}(..)'
        FakeCanvas.log.append([ref, args, kwargs])
        return FakeCanvas(ref)

    def setFont(self, psfontname, size, leading=None):
        FakeCanvas.log.append(['canvas/setFont', (psfontname, size, leading), {}])
        self._fontname = psfontname
        self._fontsize = size


@pytest.fixture
def canvas():
    c = FakeCanvas('canvas')
    FakeCanvas.log.clear()
    return c
