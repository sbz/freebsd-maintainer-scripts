PORTNAME=		freebsd-maintainer-scripts
DISTVERSION=	20210528
CATEGORIES=		ports-mgmt

MAINTAINER=		sbz@FreeBSD.org
COMMENT=		Script utilities for maintainer tasks

LICENSE=		BSD2CLAUSE
LICENSE_FILE=	${WRKSRC}/LICENSE

BUILD_DEPENDS=	distilator>0:ports-mgmt/distilator \
				python3>0:lang/python3 \
				portlint>0:ports-mgmt/portlint \
				poudriere>0:ports-mgmt/poudriere \
				${PYTHON_PKGNAMEPREFIX}python-bugzilla>0:devel/py-python-bugzilla@${PY_FLAVOR}

RUN_DEPENDS=	${BUILD_DEPENDS}

NO_BUILD=	yes
USE_GITHUB=	yes
USES=		python

GH_ACCOUNT=	sbz
GH_PROJECT=	freebsd-maintainer-scripts
GH_TAGNAME=	a0e9912

do-install:
	@${MKDIR} ${STAGEDIR}/usr/bin/
	${INSTALL_SCRIPT} ${WRKSRC}/check-distfile.sh ${STAGEDIR}${PREFIX}/bin/fms-check-distfile
	${INSTALL_SCRIPT} ${WRKSRC}/ftabs.py ${STAGEDIR}${PREFIX}/bin/fms-ftabs
	${INSTALL_SCRIPT} ${WRKSRC}/gensrc ${STAGEDIR}${PREFIX}/bin/fms-gensrc
	${INSTALL_SCRIPT} ${WRKSRC}/getprs.py ${STAGEDIR}${PREFIX}/bin/fms-getpr

.include <bsd.port.mk>
