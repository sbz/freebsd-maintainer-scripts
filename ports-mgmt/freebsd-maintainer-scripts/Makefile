PORTNAME=		freebsd-maintainer-scripts
CATEGORIES=		ports-mgmt

MAINTAINER=		sbz@FreeBSD.org
COMMENT=		Script utilities for maintainer tasks

LICENSE=		BSD
LICENSE_FILE=	${WRKSRC}/LICENSE

BUILD_DEPENDS=	distilator>0:${PORTSDIR}/ports-mgmt/distilator \
				python3>0:${PORTSDIR}/lang/python3 \
				portlint>0:${PORTSDIR}/ports-mgmt/portlint \
				poudriere>0:${PORTSDIR}/devel/poudriere

RUN_DEPENDS=	${BUILD_DEPENDS}

NO_BUILD=	yes
USE_GITHUB=	yes

GH_ACCOUNT=	sbz
GH_PROJECT=	freebsd-maintainer-scripts

build:
	mkdir -p ${STAGEDIR}/usr/bin/
	cp ${WKRSRC}/check-distfile.sh ${STAGEDIR}/usr/bin/fms-check-distfile
	cp ${WRKSRC}/ftabs.py ${STAGEDIR}/usr/bin/fms-ftabs
	cp ${WRKSRC}/gensrc ${STAGEDIR}/usr/bin/fms-gensrc

.include <bsd.port.mk>
