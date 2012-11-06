# -*- coding: utf-8 -*-
import colander
import deform


class SchemaRowZeleniIzhod(colander.TupleSchema):
    n_0 = colander.SchemaNode(colander.Float(), validator=colander.Range(0, 1))
    n_1 = colander.SchemaNode(colander.Float(), validator=colander.Range(0, 1))


class SchemaRowsZeleniIzhod(colander.SequenceSchema):
    row = SchemaRowZeleniIzhod()


class SchemaRowVhod(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsVhod(colander.SequenceSchema):
    row = SchemaRowVhod()


class SchemaRowUtez1(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_3 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsUtez1(colander.SequenceSchema):
    row = SchemaRowUtez1()


class SchemaRowUtez2(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_3 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsUtez2(colander.SequenceSchema):
    row = SchemaRowUtez2()


class SchemaNevronskaMreza(colander.MappingSchema):

    eta = colander.SchemaNode(colander.Float(),
                              validator=colander.Range(0, 1),
                              default=0.3,
                              description="Hitrost učenja")

    vhod = SchemaRowsVhod(description="Vhodne vrednosti brez biasa",
                          validator=colander.Length(1, 2),
                          title=u"Vhod",
                          widget=deform.widget.SequenceWidget(
                              min_len=1,
                              max_len=2)
                          )
    zeleni_izhod = SchemaRowsZeleniIzhod(
        description=u"Kakšen bi moral biti izhod nevronske mreže",
        #widget=deform.widget.TextAreaCSVWidget(rows=2, cols=10),
        #validator=colander.Range(1, 2, u"Vsebuje manj vrstic kot ${min}!",
                                 #u"Vsebuje več več vrstic kot ${max}!"),
    )

    utezi_prvi_nivo = SchemaRowsUtez1(validator=colander.Length(1, 3))

    utezi_drugi_nivo = SchemaRowsUtez2(validator=colander.Length(1, 2))

    utez_i = colander.SchemaNode(colander.Int(),
                                 validator=colander.Range(1, 3),
                                 default=1,
                                 description=u"w_i,j^(l) i koordinata uteži")
    utez_j = colander.SchemaNode(colander.Int(),
                                 colander=colander.Range(1, 3),
                                 default=2,
                                 description=u"w_i,j^(l) j koordinata uteži")
    utez_l = colander.SchemaNode(colander.Int(),
                                 colander=colander.Range(1, 2),
                                 default=1,
                                 description=u"w_i,j^(l) l koordinata uteži")
