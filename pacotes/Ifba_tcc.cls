%
% Classe ifba_tcc.cls para os programas de graduações e pós graduações 
% SE NÃO TEM AS MANHÃS NÃO MEXA NÃO!!!
%by: Valdex de Jesus Santos <valdexsantos@ifba.edu.br>
\PassOptionsToPackage{inline,shortlabels}{enumitem} % para corrigir conflito no enumerate personalizado no abntex
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pacotes/Ifba_tcc}[2024/07/30 v5.0]

% repassa os parametros ao abntex2
\DeclareOption*{
	\PassOptionsToClass{\CurrentOption}{abntex2}
}

\PassOptionsToClass{
	% -- opções da classe memoir --
	12pt,				% tamanho da fonte
	openright,			% capítulos começam em pág ímpar (insere página vazia caso preciso)
	a4paper,			% tamanho do papel.
	sumario=tradicional,		% seleciona o sumário tradicional
	% -- opções da classe abntex2 --
	%chapter=TITLE,			% títulos de capítulos convertidos em letras maiúsculas
	%section=TITLE,			% títulos de seções convertidos em letras maiúsculas
	%subsection=TITLE,		% títulos de subseções convertidos em letras maiúsculas
	%subsubsection=TITLE,		% títulos de subsubseções convertidos em letras maiúsculas
	% -- opções do pacote babel --
	brazil,				% o último idioma é o principal do documento
	}{abntex2}

\ProcessOptions\relax
\LoadClass{abntex2}

\RequirePackage{chngcntr}

% define a numeração das equações de forma sequencial
\counterwithout{equation}{chapter}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ESTILO DE ELEMENTOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% elementos pre-textuais
\renewcommand{\pretextual}{
	\pagenumbering{roman} % algarismos romanos
	\aliaspagestyle{chapter}{empty}%tira a numeração dos elementos pré-textuais
	\pagestyle{empty} 
	\aliaspagestyle{cleared}{empty}
	\aliaspagestyle{part}{empty}
}

% elementos textuais
% Configura layout para elementos textuais
\renewcommand{\textual}{
	\pagenumbering{arabic} % inicia a numeração em 1
	\ifthenelse{\equal{\ABNTEXisarticle}{true}}{
		\pagestyle{plain}
	}{
		\pagestyle{abntheadings}
		\aliaspagestyle{chapter}{abntchapfirst}
	}
	\nouppercaseheads
	\bookmarksetup{startatroot}
}

% elementos pos-textuais
\renewcommand{\postextual}{\phantompart}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% COMANDOS DE DADOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\logoInst}[1]{
\newcommand{\logo}{#1}
}
% comandos de dados - programa
\providecommand{\imprimirprograma}{}
\newcommand{\programa}[1]{\renewcommand{\imprimirprograma}{#1}}

\providecommand{\imprimircampus}{}
\newcommand{\campus}[1]{\renewcommand{\imprimircampus}{#1}}

\providecommand{\imprimirDepartamento}{}
\newcommand{\departamento}[1]{\renewcommand{\imprimirDepartamento}{#1}}

\providecommand{\imprimircurso}{}
\newcommand{\curso}[1]{\renewcommand{\imprimircurso}{#1}}

% comandos de dados - subtítulo
\providecommand{\imprimirsubtitulo}{}
\newcommand{\subtitulo}[1]{\renewcommand{\imprimirsubtitulo}{#1}}

%comando de título em english
\providecommand{\imprimirtitleenglish}{}
\newcommand{\titleenglish}[1]{\renewcommand{\imprimirtitleenglish}{#1}}

% comandos de dados - instituição do coorientador
\providecommand{\imprimirinstCoorientador}{}
\newcommand{\instCoorientador}[1]{\renewcommand{\imprimirinstCoorientador}{#1}}

% criação do comando para área de concentração (folha de rosto)
\newcommand{\imprimirareaconcentracaoRotulo}{\'Area de concentra\c{c}\~ao: }
\providecommand{\imprimirareaconcentracao}{}
\newcommand{\areaconcentracao}[1]{\renewcommand{\imprimirareaconcentracao}{#1}}

% criação do comando para linha de pesqusa (folha de rosto)
\newcommand{\imprimirlinhapesquisaRotulo}{Linha de pesquisa: }
\providecommand{\imprimirlinhapesquisa}{}
\newcommand{\linhapesquisa}[1]{\renewcommand{\imprimirlinhapesquisa}{#1}}

%========================================================================
%DADOS DA DEFFESA

%comando data de defesa
\providecommand{\imprimirdatadefesa}{}
\newcommand{\datadefesa}[1]{\renewcommand{\imprimirdatadefesa}{#1}}

%comandoS MEMBROS DA BANCA

\providecommand{\imprimirbancamembrointerno}{}
\newcommand{\bancamembrointerno}[1]{\renewcommand{\imprimirbancamembrointerno}{#1}}

\providecommand{\imprimirbancainstmembrointerno}{}
\newcommand{\bancainstmembrointerno}[1]{\renewcommand{\imprimirbancainstmembrointerno}{#1}}

\providecommand{\imprimirbancamembroexterno}{}
\newcommand{\bancamembroexterno}[1]{\renewcommand{\imprimirbancamembroexterno}{#1}}

\providecommand{\imprimirbancainstmembroexterno}{}
\newcommand{\bancainstmembroexterno}[1]{\renewcommand{\imprimirbancainstmembroexterno}{#1}}

%=======================================================================

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% OBJETOS FLUTUANTES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% comando que trata as notas nos objetos flutuantes
\renewcommand{\nota}[1]{
	\begin{SingleSpacing}\par\end{SingleSpacing}
	\begin{tabular}{p{.05\textwidth}p{.9\textwidth}}
		Nota: & #1
	\end{tabular}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PARÁGRAFOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% tamanho da identação do parágrafo
\setlength{\parindent}{1.3cm}

% espaçamento entre um parágrafo e outro
\setlength{\parskip}{0.2cm}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FONTES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% redefinição de fontes
\renewcommand{\ABNTEXchapterfont}{\normalfont\bfseries}
\renewcommand{\ABNTEXchapterfontsize}{\Large}

\renewcommand{\ABNTEXpartfont}{\normalfont}
\renewcommand{\ABNTEXpartfontsize}{\ABNTEXchapterfontsize}

\renewcommand{\ABNTEXsectionfont}{\normalfont}
\renewcommand{\ABNTEXsectionfontsize}{\Large}

\renewcommand{\ABNTEXsubsectionfont}{\normalfont}
\renewcommand{\ABNTEXsubsectionfontsize}{\large}

\renewcommand{\ABNTEXsubsubsectionfont}{\normalfont}
\renewcommand{\ABNTEXsubsubsectionfontsize}{\normalsize}

\renewcommand{\ABNTEXsubsubsubsectionfont}{\normalfont}
\renewcommand{\ABNTEXsubsubsubsectionfontsize}{\normalsize}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SUMÁRIO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% travessão no sumário para apêndices e anexos
\renewcommand{\cftchapteraftersnum}{\hfill{} -- \hfill{}}

% insere espaço entre os itens do sumario de diferentes capítulos
\setlength{\cftbeforechapterskip}{1.0em \@plus\p@}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LISTAS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% define os títulos das listas
\addto\captionsbrazil{
	% ajusta nomes padrões do babel
	\renewcommand{\listadesiglasname}{Lista de abreviaturas e siglas}
	\renewcommand{\listadesimbolosname}{Lista de s\'imbolos}
	\renewcommand{\listfigurename}{Lista de figuras}
	\renewcommand{\listtablename}{Lista de tabelas}
	% ajusta nomes usados com a macro \autoref
	\renewcommand{\pageautorefname}{p\'agina}
	\renewcommand{\sectionautorefname}{Se{\c c}\~ao}
	\renewcommand{\subsectionautorefname}{Subse{\c c}\~ao}
	\renewcommand{\subsubsectionautorefname}{Subse{\c c}\~ao}
	\renewcommand{\paragraphautorefname}{Subse{\c c}\~ao}
}
\newcommand{\listofquadrosname}{Lista de quadros}

% cria a lista de quadros
\newcommand{\quadroname}{Quadro}
\newfloat[chapter]{quadro}{loq}{\quadroname}
\newlistof{listofquadros}{loq}{\listofquadrosname}
\newlistentry{quadro}{loq}{0}

\counterwithout{quadro}{chapter}
\renewcommand{\cftquadroname}{\quadroname\space}
\renewcommand*{\cftquadroaftersnum}{\hfill--\hfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CAPA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
\renewcommand{\imprimircapa}{
	\begin{capa}

\hspace{-2.8cm}\begin{minipage}{0.3\textwidth}
		\begin{center}
		    \logo %inserindo a logo da instituição
		\end{center}
		\end{minipage}
		\quad
  \hspace{-1.5cm}
		\begin{minipage}{0.7\textwidth}
			\begin{center}
		      \normalfont\textbf{\MakeUppercase\imprimirinstituicao}\\%\vspace*{0.3cm}
                \ifdefempty{\imprimircampus}{}{\normalfont\textbf{\MakeUppercase\imprimircampus}\\} 
		      \ifdefempty{\imprimirprograma}{}{\normalfont\textbf{\normalfont\textbf{\MakeUppercase\imprimirprograma}}\\}
            \ifdefempty{\imprimircurso}{}{\normalfont{ \textbf{\MakeUppercase\imprimircurso}}\\} 
			\end{center}
		\end{minipage}\\
		\rule{0.95\textwidth}{.02cm}
	\vspace*{100pt}
	
	\begin{center}
				\ABNTEXchapterfont\textbf{\MakeUppercase\imprimirautor}
			\end{center}
			
		\vspace*{90pt}

		\begin{center}
			\ABNTEXchapterfont\textbf{\MakeUppercase\imprimirtitulo}
			\abntex@ifnotempty{\imprimirsubtitulo}{
				{\ABNTEXchapterfont\textbf{\hspace*{-0.3em}: }}{\ABNTEXchapterfont\imprimirsubtitulo}
			}
		\end{center}

		\vspace*{20pt}

	
		\vspace*{\fill}

		\begin{center}
			\normalfont\textbf{\large\imprimirlocal}\\
			\normalfont\textbf{\large\imprimirdata}
		\end{center}

	\end{capa}
}
\makeatother


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FOLHA DE ROSTO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
\renewcommand{\folhaderostocontent}{
	\setcounter{page}{2}
	\begin{center}
		\ABNTEXchapterfont\textbf{\MakeUppercase\imprimirautor}
	\end{center}

	\vspace*{150pt}

	\begin{center}
		\ABNTEXchapterfont\textbf{\MakeUppercase\imprimirtitulo}
		\abntex@ifnotempty{\imprimirsubtitulo}{
			{\ABNTEXchapterfont{\hspace*{-0.3em}: }}{\ABNTEXchapterfonte\imprimirsubtitulo}
		}
	\end{center}

	\vspace*{50pt}

	\abntex@ifnotempty{\imprimirpreambulo}{
		\SingleSpacing
		\begin{tabular}{p{.25\textwidth}p{.13\textwidth}p{.44\textwidth}}
			& \multicolumn{2}{p{.6\textwidth}}{\small\hyphenpenalty=10000{\imprimirpreambulo}} \\ & & \\
			\abntex@ifnotempty{\imprimirareaconcentracao}
			{
				& \multicolumn{2}{p{.6\textwidth}}{\small\hyphenpenalty=10000{\imprimirareaconcentracaoRotulo\imprimirareaconcentracao}} \\ & & \\
			}
			\abntex@ifnotempty{\imprimirlinhapesquisa}
			{
					& \multicolumn{2}{p{.6\textwidth}}{\small\hyphenpenalty=10000{\imprimirlinhapesquisaRotulo\imprimirlinhapesquisa}} \\ & & \\
			}
			& \small\imprimirorientadorRotulo & \imprimirorientador \\
			    & \small\imprimircoorientadorRotulo & \imprimircoorientador \\
			& & \small\imprimirinstCoorientador \\ & & \\
		\end{tabular}
	}

	\vspace*{\fill}

	\begin{center}
			\normalfont\textbf{\large\imprimirlocal}\\
		\normalfont\textbf{\large\imprimirdata}
	\end{center}
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DEDICATORIA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewenvironment{dedicatoria}[1][]
{
	\ifthenelse{\equal{#1}{}}{
		\PRIVATEbookmarkthis{\dedicatorianame}
	}{\pretextualchapter{#1}}

	\vspace*{\fill}

	\begin{flushright}
		\begin{minipage}{.5\textwidth}
			\begin{SingleSpacing}
				\setlength\parindent{0pt}
				\setlength\parskip{12pt}
}
{
			\end{SingleSpacing}
		\end{minipage}
	\end{flushright}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EPIGRAFE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewenvironment{epigrafe}[1][]
{
	\ifthenelse{\equal{#1}{}}{
		\PRIVATEbookmarkthis{\epigraphname}
	}{\pretextualchapter{#1}}

	\vspace*{\fill}

	\begin{flushright}
		\begin{minipage}{.5\textwidth}
			\begin{SingleSpacing}
				\setlength\parindent{0pt}
				\setlength\parskip{12pt}
}
{
			\end{SingleSpacing}
		\end{minipage}
	\end{flushright}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% IMPORTAÇÃO DE PACOTES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	\usepackage{bookmark}					% cria menu de bookmarks
	\usepackage[utf8]{inputenc}				% acentuação direta
	\usepackage[T1]{fontenc}				% codificação da fonte em 8 bits
	\usepackage{graphicx}					% inserir figuras
	\usepackage{float}				    	%PERMITE usar H em figura
	%\usepackage{picinpar}					% imagens ao lado do texto
	\usepackage{amsfonts, amssymb, amsmath}		% fonte e simbolos matemáticos
	\usepackage{cancel}                     %cancelar termos numa expressão matemática
	\usepackage{lastpage}			% Usado pela Ficha catalográfica
	\usepackage{verbatim} \usepackage{minted}					% texto é interpretado como escrito no documento
	\usepackage{multirow, array}				% múltiplas linhas e colunas em     tabelas
	\usepackage{indentfirst}				% indenta o primeiro parágrafo de cada seção.
	\usepackage[algoruled, portuguese]{algorithm2e}		% escrever algoritmos
	%\usepackage{times}				    	% usa a fonte Times
	\usepackage{hyperref} 		            % inserindo links azuis, referências em preto
	\usepackage{multicol}                   % para usar o ambiente multicols-multiplas colunas
%	\usepackage{paralist}                  %permite listas especiais
	\usepackage{xcolor, colortbl}			% comandos de cores
	%\usepackage{breakurl}					% permite quebra de linha em urls
	%PARA INCLUIR SUBFIGURAS precisa do caption e subcaption
	\usepackage{caption} 
    \usepackage{subcaption}
	\usepackage{hyperref} 	
	%\usepackage{subeqnarray}				% sub enumeração de equações
	%\usepackage{makeidx}					% produzir índice remissivo (glossario)
	%\usepackage{multind}					% produzir índices múltiplos
	\usepackage{pdfpages}               % inserir arq. pdf no texto (ex.: folha de aprovação e ficha catalográfica)
	\usepackage{pdflscape}                % permite colocar página em formato paisagem
%	\usepackage[normalem]{ulem} % para o underline colorido
        % \usepackage{natbib}
        \usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{times}
\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=2cm]{geometry}
\usepackage{array}
\usepackage{setspace}
\usepackage{caption}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{longtable}
\usepackage{graphicx} % Necessário para \rotatebox
\usepackage{lscape}   % Se quiser forçar paisagem (não vamos usar aqui)


\RequirePackage{nomencl}        % Pacote para criacao da Lista de Siglas

\usepackage{csquotes} %lida com as aspas corretamente para diferentes idiomas quando se usa o biblatex
\usepackage{titlesec} %PERMITE AJUSTAR O ESPAÇAMENTO NO TITULO DOS CAPITULOS
%===========%===================%===================%
%CONFIGURAÇÕES DE REFERENCIAS -%PACOTES PARA CITAÇÃO
\usepackage[
    backend=biber,
    style = abnt, % Sistema alfabético
    language=brazilian,
    % style = abnt-numeric, % Sistema numérico
   % justify %Imprime o texto justificado em vez de alinhado à esquerda
    hyperref,         % Referências linkadas
   %bftitles,         % descomente para immprir títulos em negrito
    noslsn,           % Oculta [s.l], [s.n] and [s.l.: s.n.]
    %nosl,             % Uncomment to hide just [s.l]
    %nosn,             % Uncomment to hide just [s.n]
 ]{biblatex}
 \renewcommand*{\mkbibnamefamily}[1]{#1}%
 \usepackage{csquotes}
\addbibresource{refbase.bib} %ARQUIVO DE REFERÊNCIAS
%===========%===================%===================%
%\usepackage{abntex2cite}
%	\usepackage[alf, abnt-emphasize=bf, bibjustif, recuo=0cm, abnt-etal-cite=2, abnt-etal-list=0]{abntex2cite}	% citações padrão ABNT

%




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% define as cores dos links e informações do pdf
\makeatletter
\hypersetup{
	portuguese,
	colorlinks,
	linkcolor=black,
	citecolor=blue,
	filecolor=blue,
	urlcolor=blue,
	breaklinks=true,
	pdftitle={\@title},
	pdfauthor={\@author},
	pdfsubject={\imprimirpreambulo},
	pdfkeywords={abnt, latex, abntex, abntex2}
}
%Ocultar advertência do biblatex
\usepackage{silence}
\WarningsOff[biblatex]



%================================================================================
% CONSTRUINDO A LISTA DE SIGLAS AUTOMÁTICA
%================================================================================
\usepackage{nomencl} %necessário para construir a lista de símbolos sigLas

% Configuracao do pacote nomencl
% Tamanho da Label da sigla
\setlength{\nomlabelwidth}{0.15\hsize}
% Separa as abreviaturas de suas definicoes com pontos (....)
\renewcommand{\nomlabel}[1]{#1 \hfill}
\setlength{\nomitemsep}{-.05in}
% Comando necessario para a criacao da lista de abreviaturas
\makenomenclature
% Traduz o titulo da lista de abreviaturas
\renewcommand{\nomname}{\listadesiglasname}

% Comando para criacao de abreviaturas e siglas
\def\sigla{\@ifstar\@sigla\@@sigla}
% Apenas faz o registro na tabela de siglas
\def\@sigla#1#2{\nomenclature{#1}{#2}}          % \sigla*{}{}
% Faz o registro na tabela de siglas e insere os dados no corpo do documento
\def\@@sigla#1#2{#2 (#1)\nomenclature{#1}{#2}}  % \sigla{}{}

% Opcao para exibir a lista de siglas
\newcommand{\incluilistadesiglas}{
  \gdef\@incluilistadesiglas{true}
}

\newcommand{\inserelistadesiglas}{
  \@ifundefined{@incluilistadesiglas}{}{
    \pdfbookmark[0]{\listadesiglasname}{listadesiglas}
    \printnomenclature
    \cleardoublepage
  }
}

%================================================
%DEFININÇÃO DA LISTA DE SIMBOLOS
%COMANDO: \simbolo{novosimbolo}{significado}

\newcommand\simbolo[2]{%
  \write\@auxout{\noexpand\@writefile{sbl}{\noexpand\item[#1] #2}}}
\newcommand\imprimirlistadesimbolos{%
  \begin{simbolos}
   \@starttoc{sbl}
  \end{simbolos}}

%================================================
%NOVOS COMANDO
\newcommand{\aspas}[1]{``#1''} %comando para aspas
\newcommand{\citeonline}[2][]{\textcite[#1]{#2}} %comando alternativo para citações usando \citeonline em vez de \textcite