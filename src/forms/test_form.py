from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

# Literals defined from the form's options for type safety and validation.

Evaluator = Literal[
    "José Alonso",
    "Martín Abreu",
    "Florencia Clemente",
    "Maria Noel Ferrer",
    "Constanza Boix",
    "Victoria Mignone",
    "Oscar de Oliveira Madeira",
    "Otras",
]

UcuCommunityMember = Literal[
    "Alumno/a",
    "Egresado/a",
    "Docente",
    "Funcionario/a",
    "Otras",
]

Faculty = Literal[
    "FIT",
    "FCS",
    "FCE",
    "FAV",
    "UCU BUSINESS",
    "Otras",
]

Stage = Literal[
    "Ideación",
    "Validación",
    "Tracción/Consolidación",
    "Crecimiento/Expansión",
    "Transformación/Spin off",
    "Otras",
]

ProfileType = Literal[
    "ANII (Disrupción y escala)",
    "ANDE (Novedad y escala)",
    "Berit (Underpriviledge)",
    'Emprendimientos común sin "novedad y escala"',
    "Impacto Social",
    "Economía Circular",
    "Impacto ambiental",
    "Otras",
]

SupportType = Literal[
    "Ningún apoyo adicional (No UCU y no valor estratégico)",
    "IPE Postulación VIN ANII/ANDE",
    "IPE Postulación Semilla ANDE",
    "IPE Emprendedores innovadores ANII",
    "Otros Financiamientos",
    "Programa de incubación general",
    "Cursos de Uruguay Emprendedor",
    "Valida Lab UCU",
    "Mentoria/Tutoría (elegir de la lista a continuación)",
    "Ingreso al catálogo de emprendimientos",
    "Acceso a laboratorios (Industrial, Alimentos Química, electrónica, IoT)",
    "Club de beneficios",
    "Centro Ignis (Industrias creativas)",
    "Comunicad UCU",
    "Actividades de Networking",
    "Tema para retos FIT",
    "Becario/s",
    "Sesión de IA (investigación mercado, estrategias, etc)",
    "Otras",
]

Mentor = Literal[
    "Luis Silveira",
    "Juan Cosido",
    "Silvia Bentancur",
    "Maria Laura Rocha",
    "Marina Correa",
    "Magdalena Balestero",
    "Federico Heuer Miller",
    "Matilde Rosello",
    "Maria Fasciolli",
    "Maria Eloisa González",
    "Ana Curutchet",
    "Bernardo Rychtenberg",
    "Otras",
]

# The "No" option is added for this specific question.
FollowUpPerson = Literal[
    "No",
    "José Alonso",
    "Martín Abreu",
    "Florencia Clemente",
    "Maria Noel Ferrer",
    "Constanza Boix",
    "Victoria Mignone",
    "Oscar de Oliveira Madeira",
    "Otras",
]


class IthakaEvaluationSupportForm(BaseModel):
    """
    ### Evaluación de ideas/emprendimientos - Comité Ithaka

    El objetivo de este formulario es sistematizar y digitalizar la evaluación de
    ideas o emprendimientos que se postulan para recibir apoyo de Ithaka.
    La dinámica del comité es que un sponsor prepara la información necesaria
    para comentar en el comité pueda entender de qué se trata, evaluar y
    proponer próximos pasos.
    """

    name: str = Field(description="The name of the person answering the survey. ")

    first_question: Literal["Evaluación primaria del Sponsor", "Comité de evaluación"] | None = (
        Field(
            default=None,
            description="Answers: ¿Es un comité de evaluación o es una evaluación del sponsor? ",
        )
    )

    date_of_completion: date | None = Field(default=None, description="Date of completion. ")

    evaluators: tuple[Evaluator | None, Evaluator | None] = Field(
        default=(None, None),
        description="Up to two evaluators of the form. ",
    )

    idea: str = Field(
        description="Answers: ¿Qué idea/emprendimiento se está evaluando? \nIncluye el ID de referencia del formulario de postulación o el nombre del/la postulante. "
    )

    sponsor: str = Field(
        description="Answers: ¿Quién es el sponsor de Ithaka para esta idea/emprendimiento? \nDetalla el nombre o apellido de la persona del equipo de ITHAKA que presenta la oportunidad de apoyo. "
    )

    ucu_community_members: tuple[UcuCommunityMember | None, UcuCommunityMember | None] = Field(
        default=(None, None),
        description="Answers: ¿El/La/Los emprendedore/a/s pertenecen a la comunidad UCU?  Up to two options. ",
    )

    linked_faculty: tuple[Faculty | None, Faculty | None] = Field(
        default=(None, None),
        description="Answers: ¿De qué carrera/facultad está vinculado?  Up to two options. ",
    )

    stage: tuple[Stage | None, Stage | None] = Field(
        default=(None, None),
        description="Answers: ¿En qué etapa está?  Up to two options. ",
    )

    profile_type: list[ProfileType] = Field(
        default=[],
        description="Answers: ¿De qué tipo de perfil es la idea/emprendimiento? ",
    )

    potential_support: list[SupportType] = Field(
        default=[],
        description="Answers: ¿Qué tipo de apoyos podemos brindarle al emprendedor/a o emprendimiento según el perfil? ",
    )

    specific_mentor: list[Mentor] = Field(
        default=[],
        description="Answers: ¿Hay algún tutor/mentor específico para apoyar esta idea/emprendimiento? ",
    )

    follow_up_personnel: tuple[FollowUpPerson | None, FollowUpPerson | None] = Field(
        default=(None, None),
        description="Answers: ¿Se asignará a alguien específico del equipo de Ithaka para el seguimiento?  Up to two options. ",
    )

    internal_comments: str = Field(
        description="Answers: ¿Cuáles son los comentarios internos de esta instancia de evaluación? "
    )

    message_for_applicant: str = Field(
        description="Answers: ¿Qué mensaje se le quiere compartir al postulante? "
    )
