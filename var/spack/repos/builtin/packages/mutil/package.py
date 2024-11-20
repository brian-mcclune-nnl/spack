# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mutil
#
# You can edit this file again by typing:
#
#     spack edit mutil
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Mutil(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://pkolano.github.io/projects/mutil.html"

    maintainers("brian-mcclune-nnl")

    # Check based on GNU coreutils.
    license("GPL-3.0-or-later", checked_by="brian-mcclune-nnl")

    version(
        "1.822.6",
        sha256="5b3e94998152c017e6c75d56b9b994188eb71bf46d4038a642cb9141f6ff1212",  # noqa: E501
        url="http://ftpmirror.gnu.org/coreutils/coreutils-8.22.tar.xz",
    )

    variant(
        "static",
        default=False,
        description="statically link libgcrypt, libgpg-error, and gnutls",
    )
    variant(
        "tcp",
        default=False,
        description="build with multi-node TCP support",
    )
    variant(
        "mpi",
        default=False,
        description="build with multi-node MPI support",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    # Version 3.5+ ensures --with-included-tasn1
    depends_on("libgcrypt@1.6.2:")
    depends_on("libgpg-error@1.17:")
    depends_on("zlib", when="+static")
    depends_on("gnutls@3.5:", when="+tcp")
    depends_on("mpi", when="+mpi")

    patch(
        "https://raw.githubusercontent.com/pkolano/mutil/edac76b163513e4b7ca7bed094f191cb6d0c1fb3/patch/coreutils-8.22.patch",  # noqa: E501
        sha256="8c8cce51cbe673d1de5278444adf044e9ed03b909414ad71843a6e32f4cc4c6d",  # noqa: E501
        when="@1.822.6",
    )
    # glibc 2.28+ removed libio.h and thus _IO_ftrylockfile
    patch("glibc-2.28-work-around.patch", when="@1.822.6")

    force_autoreconf = True

    def configure_args(self):
        args = []
        if "+static" in self.spec:
            args.append("--with-static-gcrypt")

        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(join_path(prefix.man, "man1"))
        with working_dir(self.build_directory):
            install(join_path("src", "cp"), join_path(prefix.bin, "mcp"))
            install(join_path("src", "md5sum"), join_path(prefix.bin, "msum"))
            install(
                join_path("man", "cp.1"),
                join_path(prefix.man, "man1", "mcp.1"),
            )
            install(
                join_path("man", "md5sum.1"),
                join_path(prefix.man, "man1", "msum.1"),
            )
