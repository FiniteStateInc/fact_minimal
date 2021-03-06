import logging
import os
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory

from common_helper_files import get_binary_from_file

from unpacker.unpackBase import UnpackBase


class TarRepack(UnpackBase):

    def tar_repack(self, file_path):
        extraction_directory = TemporaryDirectory(prefix='FAF_tar_repack')
        self.extract_files_from_file(file_path, extraction_directory.name)

        archive_directory = TemporaryDirectory(prefix='FAF_tar_repack')
        archive_path = os.path.join(archive_directory.name, 'download.tar.gz')
        tar_binary = self._repack_extracted_files(extraction_directory, archive_path)

        self._cleanup_directories(archive_directory, extraction_directory)

        return tar_binary

    @staticmethod
    def _repack_extracted_files(extraction_dir, out_file_path):
        with Popen('tar -C {} -cvzf {} .'.format(extraction_dir.name, out_file_path), shell=True, stdout=PIPE) as process:
            output = process.stdout.read().decode()
            logging.debug('tar -cvzf:\n {}'.format(output))

        return get_binary_from_file(out_file_path)

    def _cleanup_directories(self, archive_directory, extraction_directory):
        self.change_owner_back_to_me(extraction_directory.name, permissions='u+rw')
        extraction_directory.cleanup()

        self.change_owner_back_to_me(archive_directory.name, permissions='u+rw')
        archive_directory.cleanup()
