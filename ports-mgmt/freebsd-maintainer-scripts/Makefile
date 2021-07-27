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

GH_ACCOUNT=	sbz
GH_PROJECT=	freebsd-maintainer-scripts
GH_TAGNAME=	a0e9912

post-patch:
	@${MKDIR} ${STAGEDIR}/usr/bin/
	cp ${WRKSRC}/check-distfile.sh ${STAGEDIR}/usr/bin/fms-check-distfile
	cp ${WRKSRC}/ftabs.py ${STAGEDIR}/usr/bin/fms-ftabs
	cp ${WRKSRC}/gensrc ${STAGEDIR}/usr/bin/fms-gensrc
	cp ${WRKSRC}/getprs.py ${STAGEDIR}/usr/bin/fms-getpr

.include <bsd.port.mk>
