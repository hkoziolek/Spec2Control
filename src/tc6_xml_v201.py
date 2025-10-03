from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class AccessType(Enum):
    """
    Defines the different access types to an accessVariable.
    """

    READ_ONLY = "readOnly"
    READ_WRITE = "readWrite"


class AddDataDataHandleUnknown(Enum):
    PRESERVE = "preserve"
    DISCARD = "discard"
    IMPLEMENTATION = "implementation"


class BodyFbdActionBlockActionQualifier(Enum):
    P1 = "P1"
    N = "N"
    P0 = "P0"
    R = "R"
    S = "S"
    L = "L"
    D = "D"
    P = "P"
    DS = "DS"
    DL = "DL"
    SD = "SD"
    SL = "SL"


@dataclass
class BodyFbdActionBlockActionReference:
    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class BodyLdActionBlockActionQualifier(Enum):
    P1 = "P1"
    N = "N"
    P0 = "P0"
    R = "R"
    S = "S"
    L = "L"
    D = "D"
    P = "P"
    DS = "DS"
    DL = "DL"
    SD = "SD"
    SL = "SL"


@dataclass
class BodyLdActionBlockActionReference:
    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class BodySfcActionBlockActionQualifier(Enum):
    P1 = "P1"
    N = "N"
    P0 = "P0"
    R = "R"
    S = "S"
    L = "L"
    D = "D"
    P = "P"
    DS = "DS"
    DL = "DL"
    SD = "SD"
    SL = "SL"


@dataclass
class BodySfcActionBlockActionReference:
    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcTransitionConditionReference:
    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DataTypeEnumValuesValue:
    """
    An enumeration value used to build up enumeration types.
    """

    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class DataTypeString:
    """
    The single byte character string type.
    """

    class Meta:
        global_type = False

    length: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class DataTypeWstring:
    """
    The wide character (WORD) string type.
    """

    class Meta:
        global_type = False

    length: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class EdgeModifierType(Enum):
    """
    Defines the edge detection behaviour of a variable.
    """

    NONE = "none"
    FALLING = "falling"
    RISING = "rising"


@dataclass
class FormattedText:
    """
    Formatted text according to parts of XHTML 1.1.
    """

    class Meta:
        name = "formattedText"

    w3_org_1999_xhtml_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/1999/xhtml",
        },
    )


@dataclass
class Position:
    """
    Defines a graphical position in X, Y coordinates.
    """

    class Meta:
        name = "position"

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class PouType(Enum):
    """
    Defines the different types of a POU.
    """

    FUNCTION = "function"
    FUNCTION_BLOCK = "functionBlock"
    PROGRAM = "program"


@dataclass
class ProjectContentHeaderCoordinateInfoFbdScaling:
    class Meta:
        global_type = False

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoLdScaling:
    class Meta:
        global_type = False

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoPageSize:
    class Meta:
        global_type = False

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoSfcScaling:
    class Meta:
        global_type = False

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectFileHeader:
    class Meta:
        global_type = False

    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "companyName",
            "type": "Attribute",
            "required": True,
        },
    )
    company_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "companyURL",
            "type": "Attribute",
        },
    )
    product_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "productName",
            "type": "Attribute",
            "required": True,
        },
    )
    product_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "productVersion",
            "type": "Attribute",
            "required": True,
        },
    )
    product_release: Optional[str] = field(
        default=None,
        metadata={
            "name": "productRelease",
            "type": "Attribute",
        },
    )
    creation_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "creationDateTime",
            "type": "Attribute",
            "required": True,
        },
    )
    content_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentDescription",
            "type": "Attribute",
        },
    )


@dataclass
class RangeSigned:
    """
    Defines a range with signed bounds.
    """

    class Meta:
        name = "rangeSigned"

    lower: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    upper: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RangeUnsigned:
    """
    Defines a range with unsigned bounds.
    """

    class Meta:
        name = "rangeUnsigned"

    lower: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    upper: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class StorageModifierType(Enum):
    """
    Defines the storage mode (S/R) behaviour of a variable.
    """

    NONE = "none"
    SET = "set"
    RESET = "reset"


@dataclass
class ValueSimpleValue:
    """
    Value that can be represented as a single token string.
    """

    class Meta:
        global_type = False

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AddDataInfoInfo:
    """
    :ivar description:
    :ivar name: Unique name of the additional data element.
    :ivar version: Version of additional data, eg. schema version.
    :ivar vendor: Vendor responsible for the definition of the
        additional data element.
    """

    class Meta:
        global_type = False

    description: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    version: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vendor: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AddDataData:
    """
    :ivar any_element:
    :ivar name: Uniquely identifies the additional data element.
    :ivar handle_unknown: Recommended processor handling for unknown
        data elements. Specifies if the processor should try to preserve
        the additional data element, dismiss the element (e.g. because
        the data is invalid if not updated correctly) or use the
        processors default behaviour for unknown data.
    """

    class Meta:
        global_type = False

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    handle_unknown: Optional[AddDataDataHandleUnknown] = field(
        default=None,
        metadata={
            "name": "handleUnknown",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DataTypeEnumValues:
    class Meta:
        global_type = False

    value: list[DataTypeEnumValuesValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "min_occurs": 1,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoFbd:
    class Meta:
        global_type = False

    scaling: Optional[ProjectContentHeaderCoordinateInfoFbdScaling] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoLd:
    class Meta:
        global_type = False

    scaling: Optional[ProjectContentHeaderCoordinateInfoLdScaling] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfoSfc:
    class Meta:
        global_type = False

    scaling: Optional[ProjectContentHeaderCoordinateInfoSfcScaling] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class Value:
    """
    A generic value.
    """

    class Meta:
        name = "value"

    simple_value: Optional[ValueSimpleValue] = field(
        default=None,
        metadata={
            "name": "simpleValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    array_value: Optional["ValueArrayValue"] = field(
        default=None,
        metadata={
            "name": "arrayValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    struct_value: Optional["ValueStructValue"] = field(
        default=None,
        metadata={
            "name": "structValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class AddData:
    """
    Application specific data defined in external schemata.
    """

    class Meta:
        name = "addData"

    data: list[AddDataData] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class AddDataInfo:
    """
    List of additional data elements used in the document with description.
    """

    class Meta:
        name = "addDataInfo"

    info: list[AddDataInfoInfo] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectContentHeaderCoordinateInfo:
    class Meta:
        global_type = False

    page_size: Optional[ProjectContentHeaderCoordinateInfoPageSize] = field(
        default=None,
        metadata={
            "name": "pageSize",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    fbd: Optional[ProjectContentHeaderCoordinateInfoFbd] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    ld: Optional[ProjectContentHeaderCoordinateInfoLd] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    sfc: Optional[ProjectContentHeaderCoordinateInfoSfc] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class ValueArrayValueValue(Value):
    class Meta:
        global_type = False

    repetition_value: str = field(
        default="1",
        metadata={
            "name": "repetitionValue",
            "type": "Attribute",
        },
    )


@dataclass
class ValueStructValueValue(Value):
    class Meta:
        global_type = False

    member: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Body:
    """
    Implementation part of a POU, action or transistion.

    :ivar il:
    :ivar st:
    :ivar fbd:
    :ivar ld:
    :ivar sfc:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar worksheet_name:
    :ivar global_id:
    """

    class Meta:
        name = "body"

    il: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "IL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    st: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "ST",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    fbd: Optional["BodyFbd"] = field(
        default=None,
        metadata={
            "name": "FBD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    ld: Optional["BodyLd"] = field(
        default=None,
        metadata={
            "name": "LD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    sfc: Optional["BodySfc"] = field(
        default=None,
        metadata={
            "name": "SFC",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    worksheet_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "WorksheetName",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdComment:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdError:
    """Describes a graphical object representing a conversion error.

    Used to keep information which can not be interpreted by the
    importing system
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdLabel:
    """
    Describes a graphical object representing a jump label.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdComment:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdError:
    """Describes a graphical object representing a conversion error.

    Used to keep information which can not be interpreted by the
    importing system
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdLabel:
    """
    Describes a graphical object representing a jump label.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcComment:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcError:
    """Describes a graphical object representing a conversion error.

    Used to keep information which can not be interpreted by the
    importing system
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    content: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcLabel:
    """
    Describes a graphical object representing a jump label.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class Connection:
    """Describes a connection between the consumer element (eg.

    input variable of a function block) and the producer element (eg.
    output variable of a function block). It may contain a list of
    positions that describes the path of the connection.

    :ivar position: All positions of the directed connection path. If
        any positions are given, the list has to contain the first
        (input pin of the consumer element) as well as the last (output
        pin of the producer element).
    :ivar add_data:
    :ivar global_id:
    :ivar ref_local_id: Identifies the element the connection starts
        from.
    :ivar formal_parameter: If present: This attribute denotes the name
        of the VAR_OUTPUT / VAR_IN_OUTparameter of the pou block that is
        the start of the connection. If not present: If the refLocalId
        attribute refers to a pou block, the start of the connection is
        the first output of this block, which is not ENO. If the
        refLocalId attribute refers to any other element type, the start
        of the connection is the elements single native output.
    """

    class Meta:
        name = "connection"

    position: list[Position] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )
    ref_local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "refLocalId",
            "type": "Attribute",
            "required": True,
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
        },
    )


@dataclass
class ConnectionPointOut:
    """
    Defines a connection point on the producer side.

    :ivar rel_position: Relative position of the connection pin. Origin
        is the anchor position of the block.
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar global_id:
    """

    class Meta:
        name = "connectionPointOut"

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class DataTypeDerived:
    """
    The user defined alias type.
    """

    class Meta:
        global_type = False

    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PouInstance:
    """
    Represents a program or function block instance either running with or without
    a task.
    """

    class Meta:
        name = "pouInstance"

    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectContentHeader:
    """
    :ivar comment:
    :ivar coordinate_info:
    :ivar add_data_info:
    :ivar add_data:
    :ivar name:
    :ivar version:
    :ivar modification_date_time:
    :ivar organization:
    :ivar author:
    :ivar language: Documentation language of the project e.g. "en-US"
    """

    class Meta:
        global_type = False

    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    coordinate_info: Optional[ProjectContentHeaderCoordinateInfo] = field(
        default=None,
        metadata={
            "name": "coordinateInfo",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data_info: Optional[AddDataInfo] = field(
        default=None,
        metadata={
            "name": "addDataInfo",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    modification_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "modificationDateTime",
            "type": "Attribute",
        },
    )
    organization: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    author: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ValueArrayValue:
    """Array value consisting of a list of occurrances - value pairs"""

    class Meta:
        global_type = False

    value: list[ValueArrayValueValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ValueStructValue:
    """Struct value consisting of a list of member - value pairs"""

    class Meta:
        global_type = False

    value: list[ValueStructValueValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdActionBlockAction:
    """
    Association of an action with qualifier.

    :ivar rel_position: Relative position of the action. Origin is the
        anchor position of the action block.
    :ivar reference: Name of an action or boolean variable.
    :ivar inline: Inline implementation of an action body.
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar qualifier:
    :ivar width:
    :ivar height:
    :ivar duration:
    :ivar indicator:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    reference: Optional[BodyFbdActionBlockActionReference] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    inline: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    qualifier: BodyFbdActionBlockActionQualifier = field(
        default=BodyFbdActionBlockActionQualifier.N,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    indicator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdBlockOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdContinuation:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdInVariable:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdVendorElementOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdActionBlockAction:
    """
    Association of an action with qualifier.

    :ivar rel_position: Relative position of the action. Origin is the
        anchor position of the action block.
    :ivar reference: Name of an action or boolean variable.
    :ivar inline: Inline implementation of an action body.
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar qualifier:
    :ivar width:
    :ivar height:
    :ivar duration:
    :ivar indicator:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    reference: Optional[BodyLdActionBlockActionReference] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    inline: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    qualifier: BodyLdActionBlockActionQualifier = field(
        default=BodyLdActionBlockActionQualifier.N,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    indicator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdBlockOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdContinuation:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdInVariable:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdLeftPowerRailConnectionPointOut(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodyLdVendorElementOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcActionBlockAction:
    """
    Association of an action with qualifier.

    :ivar rel_position: Relative position of the action. Origin is the
        anchor position of the action block.
    :ivar reference: Name of an action or boolean variable.
    :ivar inline: Inline implementation of an action body.
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar qualifier:
    :ivar width:
    :ivar height:
    :ivar duration:
    :ivar indicator:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    reference: Optional[BodySfcActionBlockActionReference] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    inline: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    qualifier: BodySfcActionBlockActionQualifier = field(
        default=BodySfcActionBlockActionQualifier.N,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    indicator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcBlockOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcContinuation:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcInVariable:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcLeftPowerRailConnectionPointOut(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcSelectionDivergenceConnectionPointOut(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcSimultaneousDivergenceConnectionPointOut(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcStepConnectionPointOut(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcStepConnectionPointOutAction(ConnectionPointOut):
    class Meta:
        global_type = False

    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcTransitionConditionInline(Body):
    class Meta:
        global_type = False

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BodySfcVendorElementOutputVariablesVariable:
    """
    Describes a outputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ConnectionPointIn:
    """
    Defines a connection point on the consumer side.

    :ivar rel_position: Relative position of the connection pin. Origin
        is the anchor position of the block.
    :ivar connection:
    :ivar expression: The operand is a valid iec variable e.g. avar[0]
        or an iec expression or multiple token text e.g. a + b (*sum*).
        An iec 61131-3 parser has to be used to extract variable
        information.
    :ivar add_data:
    :ivar global_id:
    """

    class Meta:
        name = "connectionPointIn"

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection: list[Connection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class DataType:
    """
    A generic data type.

    :ivar bool_value:
    :ivar byte:
    :ivar word:
    :ivar dword:
    :ivar lword:
    :ivar sint:
    :ivar int_value:
    :ivar dint:
    :ivar lint:
    :ivar usint:
    :ivar uint:
    :ivar udint:
    :ivar ulint:
    :ivar real:
    :ivar lreal:
    :ivar time:
    :ivar date:
    :ivar dt:
    :ivar tod:
    :ivar string:
    :ivar wstring:
    :ivar any:
    :ivar any_derived:
    :ivar any_elementary:
    :ivar any_magnitude:
    :ivar any_num:
    :ivar any_real:
    :ivar any_int:
    :ivar any_bit:
    :ivar any_string:
    :ivar any_date:
    :ivar array:
    :ivar derived: Reference to a user defined datatype or POU. Variable
        declarations use this type to declare e.g. function block
        instances.
    :ivar enum:
    :ivar struct:
    :ivar subrange_signed:
    :ivar subrange_unsigned:
    :ivar pointer:
    """

    class Meta:
        name = "dataType"

    bool_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "BOOL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    byte: Optional[object] = field(
        default=None,
        metadata={
            "name": "BYTE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    word: Optional[object] = field(
        default=None,
        metadata={
            "name": "WORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    dword: Optional[object] = field(
        default=None,
        metadata={
            "name": "DWORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    lword: Optional[object] = field(
        default=None,
        metadata={
            "name": "LWORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    sint: Optional[object] = field(
        default=None,
        metadata={
            "name": "SINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    int_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "INT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    dint: Optional[object] = field(
        default=None,
        metadata={
            "name": "DINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    lint: Optional[object] = field(
        default=None,
        metadata={
            "name": "LINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    usint: Optional[object] = field(
        default=None,
        metadata={
            "name": "USINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    uint: Optional[object] = field(
        default=None,
        metadata={
            "name": "UINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    udint: Optional[object] = field(
        default=None,
        metadata={
            "name": "UDINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    ulint: Optional[object] = field(
        default=None,
        metadata={
            "name": "ULINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    real: Optional[object] = field(
        default=None,
        metadata={
            "name": "REAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    lreal: Optional[object] = field(
        default=None,
        metadata={
            "name": "LREAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    time: Optional[object] = field(
        default=None,
        metadata={
            "name": "TIME",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    date: Optional[object] = field(
        default=None,
        metadata={
            "name": "DATE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    dt: Optional[object] = field(
        default=None,
        metadata={
            "name": "DT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    tod: Optional[object] = field(
        default=None,
        metadata={
            "name": "TOD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    string: Optional[DataTypeString] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    wstring: Optional[DataTypeWstring] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_derived: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_DERIVED",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_elementary: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_ELEMENTARY",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_magnitude: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_MAGNITUDE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_num: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_NUM",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_real: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_REAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_int: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_INT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_bit: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_BIT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_string: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_STRING",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    any_date: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_DATE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    array: Optional["DataTypeArray"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    derived: Optional[DataTypeDerived] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    enum: Optional["DataTypeEnum"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    struct: Optional["VarListPlain"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    subrange_signed: Optional["DataTypeSubrangeSigned"] = field(
        default=None,
        metadata={
            "name": "subrangeSigned",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    subrange_unsigned: Optional["DataTypeSubrangeUnsigned"] = field(
        default=None,
        metadata={
            "name": "subrangeUnsigned",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    pointer: Optional["DataTypePointer"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectInstancesConfigurationsConfigurationResourceTask:
    """
    Represents a periodic or triggered task.

    :ivar pou_instance:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar single:
    :ivar interval: Vendor specific: Either a constant duration as
        defined in the IEC or variable name.
    :ivar priority:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    pou_instance: list[PouInstance] = field(
        default_factory=list,
        metadata={
            "name": "pouInstance",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    single: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    interval: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 65535,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectTypesPousPouActionsAction:
    """
    :ivar body:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectTypesPousPouTransitionsTransition:
    """
    :ivar body:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdActionBlock:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar action:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar negated:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action: list[BodyFbdActionBlockAction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdBlockInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdBlockInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdBlockOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdBlockOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdConnector:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdInOutVariable:
    """
    Describes a graphical object representing a variable which can be used as
    l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated_in:
    :ivar edge_in:
    :ivar storage_in:
    :ivar negated_out:
    :ivar edge_out:
    :ivar storage_out:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated_in: bool = field(
        default=False,
        metadata={
            "name": "negatedIn",
            "type": "Attribute",
        },
    )
    edge_in: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeIn",
            "type": "Attribute",
        },
    )
    storage_in: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageIn",
            "type": "Attribute",
        },
    )
    negated_out: bool = field(
        default=False,
        metadata={
            "name": "negatedOut",
            "type": "Attribute",
        },
    )
    edge_out: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeOut",
            "type": "Attribute",
        },
    )
    storage_out: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageOut",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdJump:
    """
    Describes a graphical object representing a jump statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdOutVariable:
    """
    Describes a graphical object representing a variable or expression used as
    l-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdReturn:
    """
    Describes a graphical object representing areturn statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdVendorElementInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdVendorElementInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdVendorElementOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdVendorElementOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdActionBlock:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar action:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar negated:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action: list[BodyLdActionBlockAction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdBlockInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdBlockInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdBlockOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdBlockOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdCoil:
    """
    Describes a graphical object representing a boolean variable which can be used
    as l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar variable: The operand is a valid boolean  iec variable e.g.
        avar[0]
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    variable: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdConnector:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdContact:
    """
    Describes a graphical object representing a variable which can be used as
    l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar variable: The operand is a valid boolean iec variable e.g.
        avar[0]
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    variable: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdInOutVariable:
    """
    Describes a graphical object representing a variable which can be used as
    l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated_in:
    :ivar edge_in:
    :ivar storage_in:
    :ivar negated_out:
    :ivar edge_out:
    :ivar storage_out:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated_in: bool = field(
        default=False,
        metadata={
            "name": "negatedIn",
            "type": "Attribute",
        },
    )
    edge_in: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeIn",
            "type": "Attribute",
        },
    )
    storage_in: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageIn",
            "type": "Attribute",
        },
    )
    negated_out: bool = field(
        default=False,
        metadata={
            "name": "negatedOut",
            "type": "Attribute",
        },
    )
    edge_out: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeOut",
            "type": "Attribute",
        },
    )
    storage_out: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageOut",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdJump:
    """
    Describes a graphical object representing a jump statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdLeftPowerRail:
    """
    Describes a graphical object representing a left powerrail.

    :ivar position:
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: list[BodyLdLeftPowerRailConnectionPointOut] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdOutVariable:
    """
    Describes a graphical object representing a variable or expression used as
    l-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdReturn:
    """
    Describes a graphical object representing areturn statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdRightPowerRail:
    """
    Describes a graphical object representing a right powerrail.

    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: list[ConnectionPointIn] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdVendorElementInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdVendorElementInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdVendorElementOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdVendorElementOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcActionBlock:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar action:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar negated:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action: list[BodySfcActionBlockAction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcBlockInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcBlockInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcBlockOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcBlockOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcCoil:
    """
    Describes a graphical object representing a boolean variable which can be used
    as l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar variable: The operand is a valid boolean  iec variable e.g.
        avar[0]
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    variable: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcConnector:
    """
    Describes a graphical object representing a variable, literal or expression
    used as r-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar name: The operand is a valid iec variable e.g. avar[0]
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcContact:
    """
    Describes a graphical object representing a variable which can be used as
    l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar variable: The operand is a valid boolean iec variable e.g.
        avar[0]
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    variable: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcInOutVariable:
    """
    Describes a graphical object representing a variable which can be used as
    l-value and r-value at the same time.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated_in:
    :ivar edge_in:
    :ivar storage_in:
    :ivar negated_out:
    :ivar edge_out:
    :ivar storage_out:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated_in: bool = field(
        default=False,
        metadata={
            "name": "negatedIn",
            "type": "Attribute",
        },
    )
    edge_in: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeIn",
            "type": "Attribute",
        },
    )
    storage_in: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageIn",
            "type": "Attribute",
        },
    )
    negated_out: bool = field(
        default=False,
        metadata={
            "name": "negatedOut",
            "type": "Attribute",
        },
    )
    edge_out: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "name": "edgeOut",
            "type": "Attribute",
        },
    )
    storage_out: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "name": "storageOut",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcJump:
    """
    Describes a graphical object representing a jump statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcJumpStep:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar target_name:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    target_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "targetName",
            "type": "Attribute",
            "required": True,
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcLeftPowerRail:
    """
    Describes a graphical object representing a left powerrail.

    :ivar position:
    :ivar connection_point_out:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_out: list[BodySfcLeftPowerRailConnectionPointOut] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcMacroStep:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar body:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar name:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcOutVariable:
    """
    Describes a graphical object representing a variable or expression used as
    l-value.

    :ivar position:
    :ivar connection_point_in:
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id:
    :ivar negated:
    :ivar edge:
    :ivar storage:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcReturn:
    """
    Describes a graphical object representing areturn statement.
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcRightPowerRail:
    """
    Describes a graphical object representing a right powerrail.

    :ivar position:
    :ivar connection_point_in:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: list[ConnectionPointIn] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcSelectionConvergenceConnectionPointIn(ConnectionPointIn):
    class Meta:
        global_type = False


@dataclass
class BodySfcSelectionDivergence:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: list[
        BodySfcSelectionDivergenceConnectionPointOut
    ] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcSimultaneousConvergence:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: list[ConnectionPointIn] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcSimultaneousDivergence:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: list[
        BodySfcSimultaneousDivergenceConnectionPointOut
    ] = field(
        default_factory=list,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcStep:
    """
    Contains actions.

    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar connection_point_out_action:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar name:
    :ivar initial_step:
    :ivar negated:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[BodySfcStepConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out_action: Optional[
        BodySfcStepConnectionPointOutAction
    ] = field(
        default=None,
        metadata={
            "name": "connectionPointOutAction",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    initial_step: bool = field(
        default=False,
        metadata={
            "name": "initialStep",
            "type": "Attribute",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcTransitionCondition:
    class Meta:
        global_type = False

    reference: Optional[BodySfcTransitionConditionReference] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    inline: Optional[BodySfcTransitionConditionInline] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcVendorElementInOutVariablesVariable:
    """
    Describes a inOutVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcVendorElementInputVariablesVariable:
    """
    Describes an inputVariable of a Function or a FunctionBlock.
    """

    class Meta:
        global_type = False

    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
            "required": True,
        },
    )
    negated: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    edge: EdgeModifierType = field(
        default=EdgeModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    storage: StorageModifierType = field(
        default=StorageModifierType.NONE,
        metadata={
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcVendorElementOutputVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcVendorElementOutputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class DataTypeArray:
    class Meta:
        global_type = False

    dimension: list[RangeSigned] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "min_occurs": 1,
        },
    )
    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class DataTypeEnum:
    class Meta:
        global_type = False

    values: Optional[DataTypeEnumValues] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class DataTypePointer:
    class Meta:
        global_type = False

    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class DataTypeSubrangeSigned:
    class Meta:
        global_type = False

    range: Optional[RangeSigned] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class DataTypeSubrangeUnsigned:
    class Meta:
        global_type = False

    range: Optional[RangeUnsigned] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class ProjectTypesDataTypesDataType:
    """
    :ivar base_type:
    :ivar initial_value:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    """

    class Meta:
        global_type = False

    base_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    initial_value: Optional[Value] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectTypesPousPouActions:
    class Meta:
        global_type = False

    action: list[ProjectTypesPousPouActionsAction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectTypesPousPouTransitions:
    class Meta:
        global_type = False

    transition: list[ProjectTypesPousPouTransitionsTransition] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class VarListAccessAccessVariable:
    """
    Declaration of an access variable.

    :ivar type_value:
    :ivar add_data:
    :ivar documentation:
    :ivar alias: Name that is visible to the communication partner
    :ivar instance_path_and_name: Variable name including instance path
        inside the configuration
    :ivar direction:
    """

    class Meta:
        global_type = False

    type_value: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    alias: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    instance_path_and_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instancePathAndName",
            "type": "Attribute",
            "required": True,
        },
    )
    direction: Optional[AccessType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class VarListConfigConfigVariable:
    """
    Declaration of an access variable.

    :ivar type_value:
    :ivar initial_value:
    :ivar add_data:
    :ivar documentation:
    :ivar instance_path_and_name: Variable name including instance path
    :ivar address:
    """

    class Meta:
        global_type = False

    type_value: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    initial_value: Optional[Value] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    instance_path_and_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instancePathAndName",
            "type": "Attribute",
            "required": True,
        },
    )
    address: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class VarListPlainVariable:
    """
    Declaration of a variable.
    """

    class Meta:
        global_type = False

    type_value: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    initial_value: Optional[Value] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    address: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdBlockInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdBlockInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdBlockInputVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdBlockInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdVendorElementInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdVendorElementInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdVendorElementInputVariables:
    class Meta:
        global_type = False

    variable: list[BodyFbdVendorElementInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdBlockInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdBlockInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdBlockInputVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdBlockInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdVendorElementInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdVendorElementInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLdVendorElementInputVariables:
    class Meta:
        global_type = False

    variable: list[BodyLdVendorElementInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcBlockInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcBlockInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcBlockInputVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcBlockInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcSelectionConvergence:
    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: list[BodySfcSelectionConvergenceConnectionPointIn] = (
        field(
            default_factory=list,
            metadata={
                "name": "connectionPointIn",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            },
        )
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcTransition:
    """
    :ivar position:
    :ivar connection_point_in:
    :ivar connection_point_out:
    :ivar condition:
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar height:
    :ivar width:
    :ivar priority: The priority of a transition is evaluated, if the
        transition is connected to a selectionDivergence element.
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    connection_point_in: Optional[ConnectionPointIn] = field(
        default=None,
        metadata={
            "name": "connectionPointIn",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connection_point_out: Optional[ConnectionPointOut] = field(
        default=None,
        metadata={
            "name": "connectionPointOut",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    condition: Optional[BodySfcTransitionCondition] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcVendorElementInOutVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcVendorElementInOutVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfcVendorElementInputVariables:
    class Meta:
        global_type = False

    variable: list[BodySfcVendorElementInputVariablesVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectTypesDataTypes:
    class Meta:
        global_type = False

    data_type: list[ProjectTypesDataTypesDataType] = field(
        default_factory=list,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class VarListAccess:
    """
    List of access variable declarations.
    """

    class Meta:
        name = "varListAccess"

    access_variable: list[VarListAccessAccessVariable] = field(
        default_factory=list,
        metadata={
            "name": "accessVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class VarListConfig:
    """
    List of VAR_CONFIG variables.
    """

    class Meta:
        name = "varListConfig"

    config_variable: list[VarListConfigConfigVariable] = field(
        default_factory=list,
        metadata={
            "name": "configVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class VarListPlain:
    """
    List of variable declarations without attributes.
    """

    class Meta:
        name = "varListPlain"

    variable: list[VarListPlainVariable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyFbdBlock:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar type_name:
    :ivar instance_name:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodyFbdBlockInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    in_out_variables: Optional[BodyFbdBlockInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    output_variables: Optional[BodyFbdBlockOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
            "required": True,
        },
    )
    instance_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceName",
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbdVendorElement:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar alternative_text: An alternative text to be displayed in
        generic representation of unknown elements.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data: Additional, vendor specific data for the element.
        Also defines the vendor specific meaning of the element.
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    alternative_text: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "alternativeText",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodyFbdVendorElementInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variables: Optional[BodyFbdVendorElementInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    output_variables: Optional[BodyFbdVendorElementOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdBlock:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar type_name:
    :ivar instance_name:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodyLdBlockInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    in_out_variables: Optional[BodyLdBlockInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    output_variables: Optional[BodyLdBlockOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
            "required": True,
        },
    )
    instance_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceName",
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodyLdVendorElement:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar alternative_text: An alternative text to be displayed in
        generic representation of unknown elements.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data: Additional, vendor specific data for the element.
        Also defines the vendor specific meaning of the element.
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    alternative_text: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "alternativeText",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodyLdVendorElementInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variables: Optional[BodyLdVendorElementInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    output_variables: Optional[BodyLdVendorElementOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcBlock:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data:
    :ivar documentation:
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar type_name:
    :ivar instance_name:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodySfcBlockInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    in_out_variables: Optional[BodySfcBlockInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    output_variables: Optional[BodySfcBlockOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
            "required": True,
        },
    )
    instance_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceName",
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class BodySfcVendorElement:
    """
    Describes a graphical object representing a call statement.

    :ivar position: Anchor position of the box. Top left corner
        excluding the instance name.
    :ivar alternative_text: An alternative text to be displayed in
        generic representation of unknown elements.
    :ivar input_variables: The list of used input variables (consumers)
    :ivar in_out_variables: The list of used inOut variables
    :ivar output_variables: The list of used output variables
        (producers)
    :ivar add_data: Additional, vendor specific data for the element.
        Also defines the vendor specific meaning of the element.
    :ivar local_id:
    :ivar width:
    :ivar height:
    :ivar execution_order_id: Used to identify the order of execution.
        Also used to identify one special block if there are several
        blocks with the same name.
    :ivar global_id:
    """

    class Meta:
        global_type = False

    position: Optional[Position] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    alternative_text: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "alternativeText",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    input_variables: Optional[BodySfcVendorElementInputVariables] = field(
        default=None,
        metadata={
            "name": "inputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variables: Optional[BodySfcVendorElementInOutVariables] = field(
        default=None,
        metadata={
            "name": "inOutVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    output_variables: Optional[BodySfcVendorElementOutputVariables] = field(
        default=None,
        metadata={
            "name": "outputVariables",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "localId",
            "type": "Attribute",
            "required": True,
        },
    )
    width: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    execution_order_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "executionOrderId",
            "type": "Attribute",
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class VarList(VarListPlain):
    """
    List of variable declarations that share the same memory attributes (CONSTANT,
    RETAIN, NON_RETAIN, PERSISTENT)
    """

    class Meta:
        name = "varList"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    constant: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    retain: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    nonretain: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    persistent: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    nonpersistent: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class BodyFbd:
    """
    :ivar comment:
    :ivar error:
    :ivar connector:
    :ivar continuation: Counterpart of the connector element
    :ivar action_block:
    :ivar vendor_element:
    :ivar block:
    :ivar in_variable: Expression used as producer
    :ivar out_variable: Expression used as consumer
    :ivar in_out_variable: Expression used as producer and consumer
    :ivar label:
    :ivar jump:
    :ivar return_value:
    """

    class Meta:
        global_type = False

    comment: list[BodyFbdComment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    error: list[BodyFbdError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connector: list[BodyFbdConnector] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    continuation: list[BodyFbdContinuation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action_block: list[BodyFbdActionBlock] = field(
        default_factory=list,
        metadata={
            "name": "actionBlock",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    vendor_element: list[BodyFbdVendorElement] = field(
        default_factory=list,
        metadata={
            "name": "vendorElement",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    block: list[BodyFbdBlock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_variable: list[BodyFbdInVariable] = field(
        default_factory=list,
        metadata={
            "name": "inVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    out_variable: list[BodyFbdOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "outVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variable: list[BodyFbdInOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "inOutVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    label: list[BodyFbdLabel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    jump: list[BodyFbdJump] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    return_value: list[BodyFbdReturn] = field(
        default_factory=list,
        metadata={
            "name": "return",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodyLd:
    """
    :ivar comment:
    :ivar error:
    :ivar connector:
    :ivar continuation: Counterpart of the connector element
    :ivar action_block:
    :ivar vendor_element:
    :ivar block:
    :ivar in_variable: Expression used as producer
    :ivar out_variable: Expression used as consumer
    :ivar in_out_variable: Expression used as producer and consumer
    :ivar label:
    :ivar jump:
    :ivar return_value:
    :ivar left_power_rail:
    :ivar right_power_rail:
    :ivar coil:
    :ivar contact:
    """

    class Meta:
        global_type = False

    comment: list[BodyLdComment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    error: list[BodyLdError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connector: list[BodyLdConnector] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    continuation: list[BodyLdContinuation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action_block: list[BodyLdActionBlock] = field(
        default_factory=list,
        metadata={
            "name": "actionBlock",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    vendor_element: list[BodyLdVendorElement] = field(
        default_factory=list,
        metadata={
            "name": "vendorElement",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    block: list[BodyLdBlock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_variable: list[BodyLdInVariable] = field(
        default_factory=list,
        metadata={
            "name": "inVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    out_variable: list[BodyLdOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "outVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variable: list[BodyLdInOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "inOutVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    label: list[BodyLdLabel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    jump: list[BodyLdJump] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    return_value: list[BodyLdReturn] = field(
        default_factory=list,
        metadata={
            "name": "return",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    left_power_rail: list[BodyLdLeftPowerRail] = field(
        default_factory=list,
        metadata={
            "name": "leftPowerRail",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    right_power_rail: list[BodyLdRightPowerRail] = field(
        default_factory=list,
        metadata={
            "name": "rightPowerRail",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    coil: list[BodyLdCoil] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    contact: list[BodyLdContact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class BodySfc:
    """
    :ivar comment:
    :ivar error:
    :ivar connector:
    :ivar continuation: Counterpart of the connector element
    :ivar action_block:
    :ivar vendor_element:
    :ivar block:
    :ivar in_variable: Expression used as producer
    :ivar out_variable: Expression used as consumer
    :ivar in_out_variable: Expression used as producer and consumer
    :ivar label:
    :ivar jump:
    :ivar return_value:
    :ivar left_power_rail:
    :ivar right_power_rail:
    :ivar coil:
    :ivar contact:
    :ivar step: A single step in a SFC Sequence. Actions are associated
        with a step by using an actionBlock element with a connection to
        the step element
    :ivar macro_step:
    :ivar jump_step: Jump to a step, macro step or simultaneous
        divergence. Acts like a step. Predecessor should be a
        transition.
    :ivar transition:
    :ivar selection_divergence:
    :ivar selection_convergence:
    :ivar simultaneous_divergence:
    :ivar simultaneous_convergence:
    """

    class Meta:
        global_type = False

    comment: list[BodySfcComment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    error: list[BodySfcError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    connector: list[BodySfcConnector] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    continuation: list[BodySfcContinuation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    action_block: list[BodySfcActionBlock] = field(
        default_factory=list,
        metadata={
            "name": "actionBlock",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    vendor_element: list[BodySfcVendorElement] = field(
        default_factory=list,
        metadata={
            "name": "vendorElement",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    block: list[BodySfcBlock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_variable: list[BodySfcInVariable] = field(
        default_factory=list,
        metadata={
            "name": "inVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    out_variable: list[BodySfcOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "outVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_variable: list[BodySfcInOutVariable] = field(
        default_factory=list,
        metadata={
            "name": "inOutVariable",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    label: list[BodySfcLabel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    jump: list[BodySfcJump] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    return_value: list[BodySfcReturn] = field(
        default_factory=list,
        metadata={
            "name": "return",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    left_power_rail: list[BodySfcLeftPowerRail] = field(
        default_factory=list,
        metadata={
            "name": "leftPowerRail",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    right_power_rail: list[BodySfcRightPowerRail] = field(
        default_factory=list,
        metadata={
            "name": "rightPowerRail",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    coil: list[BodySfcCoil] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    contact: list[BodySfcContact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    step: list[BodySfcStep] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    macro_step: list[BodySfcMacroStep] = field(
        default_factory=list,
        metadata={
            "name": "macroStep",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    jump_step: list[BodySfcJumpStep] = field(
        default_factory=list,
        metadata={
            "name": "jumpStep",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    transition: list[BodySfcTransition] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    selection_divergence: list[BodySfcSelectionDivergence] = field(
        default_factory=list,
        metadata={
            "name": "selectionDivergence",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    selection_convergence: list[BodySfcSelectionConvergence] = field(
        default_factory=list,
        metadata={
            "name": "selectionConvergence",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    simultaneous_divergence: list[BodySfcSimultaneousDivergence] = field(
        default_factory=list,
        metadata={
            "name": "simultaneousDivergence",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    simultaneous_convergence: list[BodySfcSimultaneousConvergence] = field(
        default_factory=list,
        metadata={
            "name": "simultaneousConvergence",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectInstancesConfigurationsConfigurationResource:
    """
    Represents a group of programs and tasks and global variables.

    :ivar task:
    :ivar global_vars:
    :ivar pou_instance:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    task: list[ProjectInstancesConfigurationsConfigurationResourceTask] = (
        field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            },
        )
    )
    global_vars: list[VarList] = field(
        default_factory=list,
        metadata={
            "name": "globalVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    pou_instance: list[PouInstance] = field(
        default_factory=list,
        metadata={
            "name": "pouInstance",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectTypesPousPouInterfaceExternalVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceGlobalVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceInOutVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceInputVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceLocalVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceOutputVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectTypesPousPouInterfaceTempVars(VarList):
    class Meta:
        global_type = False


@dataclass
class ProjectInstancesConfigurationsConfiguration:
    """
    Represents a group of resources and global variables.

    :ivar resource:
    :ivar global_vars:
    :ivar access_vars:
    :ivar config_vars:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    resource: list[ProjectInstancesConfigurationsConfigurationResource] = (
        field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            },
        )
    )
    global_vars: list[VarList] = field(
        default_factory=list,
        metadata={
            "name": "globalVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    access_vars: Optional[VarListAccess] = field(
        default=None,
        metadata={
            "name": "accessVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    config_vars: Optional[VarListConfig] = field(
        default=None,
        metadata={
            "name": "configVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectTypesPousPouInterface:
    """
    :ivar return_type:
    :ivar local_vars:
    :ivar temp_vars:
    :ivar input_vars:
    :ivar output_vars:
    :ivar in_out_vars:
    :ivar external_vars:
    :ivar global_vars:
    :ivar access_vars:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    """

    class Meta:
        global_type = False

    return_type: Optional[DataType] = field(
        default=None,
        metadata={
            "name": "returnType",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    local_vars: list[ProjectTypesPousPouInterfaceLocalVars] = field(
        default_factory=list,
        metadata={
            "name": "localVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    temp_vars: list[ProjectTypesPousPouInterfaceTempVars] = field(
        default_factory=list,
        metadata={
            "name": "tempVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    input_vars: list[ProjectTypesPousPouInterfaceInputVars] = field(
        default_factory=list,
        metadata={
            "name": "inputVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    output_vars: list[ProjectTypesPousPouInterfaceOutputVars] = field(
        default_factory=list,
        metadata={
            "name": "outputVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    in_out_vars: list[ProjectTypesPousPouInterfaceInOutVars] = field(
        default_factory=list,
        metadata={
            "name": "inOutVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    external_vars: list[ProjectTypesPousPouInterfaceExternalVars] = field(
        default_factory=list,
        metadata={
            "name": "externalVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    global_vars: list[ProjectTypesPousPouInterfaceGlobalVars] = field(
        default_factory=list,
        metadata={
            "name": "globalVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    access_vars: list[VarList] = field(
        default_factory=list,
        metadata={
            "name": "accessVars",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectInstancesConfigurations:
    class Meta:
        global_type = False

    configuration: list[ProjectInstancesConfigurationsConfiguration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectTypesPousPou:
    """
    :ivar interface:
    :ivar actions:
    :ivar transitions:
    :ivar body:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar name:
    :ivar pou_type:
    :ivar global_id:
    """

    class Meta:
        global_type = False

    interface: Optional[ProjectTypesPousPouInterface] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    actions: Optional[ProjectTypesPousPouActions] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    transitions: Optional[ProjectTypesPousPouTransitions] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    body: list[Body] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    pou_type: Optional[PouType] = field(
        default=None,
        metadata={
            "name": "pouType",
            "type": "Attribute",
            "required": True,
        },
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        },
    )


@dataclass
class ProjectInstances:
    class Meta:
        global_type = False

    configurations: Optional[ProjectInstancesConfigurations] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class ProjectTypesPous:
    class Meta:
        global_type = False

    pou: list[ProjectTypesPousPou] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        },
    )


@dataclass
class ProjectTypes:
    class Meta:
        global_type = False

    data_types: Optional[ProjectTypesDataTypes] = field(
        default=None,
        metadata={
            "name": "dataTypes",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )
    pous: Optional[ProjectTypesPous] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
            "required": True,
        },
    )


@dataclass
class Project:
    """
    The complete project.

    :ivar file_header:
    :ivar content_header:
    :ivar types:
    :ivar instances:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    """

    class Meta:
        name = "project"
        namespace = "http://www.plcopen.org/xml/tc6_0201"

    file_header: Optional[ProjectFileHeader] = field(
        default=None,
        metadata={
            "name": "fileHeader",
            "type": "Element",
            "required": True,
        },
    )
    content_header: Optional[ProjectContentHeader] = field(
        default=None,
        metadata={
            "name": "contentHeader",
            "type": "Element",
            "required": True,
        },
    )
    types: Optional[ProjectTypes] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    instances: Optional[ProjectInstances] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
        },
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
